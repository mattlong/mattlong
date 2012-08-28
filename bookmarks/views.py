import json

from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render

from toolbox import JsonResponse

from bookmarks.models import Bookmark

def add_bookmarklet(request):
    context = { 'server_host': request.META.get('HTTP_HOST') }
    return render(request, 'bookmarks/setup.html', context)

def all(request, status='NEW'):
    bookmarks = Bookmark.objects.filter(status='NEW').order_by('-created_date')
    return list_bookmarks(request, bookmarks=bookmarks)

def list_bookmarks(request, bookmarks=None):
    if not bookmarks: raise Http404()

    #for b in bookmarks:
    #    print b.url, type(b.meta_url), b.meta_url

    context = {}
    context['bookmarks'] = bookmarks
    return render(request, 'bookmarks/list.html', context)

def find(request):
    query = request.GET.get('q', '')

    if not query:
        bookmarks = Bookmark.objects.filter(status='NEW').order_by('-created_date')
    else:
        title_q = Q(title__contains=query)
        url_q = Q(url__contains=query)
        tag_q = Q(tags__text=query)
        bookmarks = Bookmark.objects.filter(title_q | url_q | tag_q).order_by('-created_date')

    return JsonResponse(bookmarks)

def add_url(request):
    callback = request.GET.get('callback')
    title = request.GET.get('title')
    url = request.GET.get('url')
    tags = request.GET.get('tags', u'').split(',')
    metaurl = request.GET.get('metaurl', u'null').lower()
    metaurl = None if metaurl.lower() == u'null' else metaurl

    if not callback or not url:
        return HttpResponse('missing params', status=400)

    data = { 'status': 'ok' }

    try:
        bookmark = Bookmark.objects.get(url=url)
    except Bookmark.DoesNotExist:
        bookmark = Bookmark(title=title, url=url, meta_url=metaurl)
        bookmark.save()

    for tag in tags:
        if tag:
            bookmark.tags.get_or_create(text=tag)

    bookmark.save()
    return HttpResponse('%s(%s);' % (callback,json.dumps(data),), content_type='application/javascript')
