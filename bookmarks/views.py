import json

from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render

from toolbox import JsonResponse, require_superuser

from bookmarks.models import Bookmark, BookmarkTag

@require_superuser
def setup_bookmarklet(request):
    context = { 'server_host': request.META.get('HTTP_HOST', 'mattlong.org') }
    return render(request, 'bookmarks/setup.html', context)

def all(request, status='NEW'):
    bookmarks = Bookmark.objects.filter(status='NEW').order_by('-created_date')
    return list_bookmarks(request, bookmarks=bookmarks)

def list_bookmarks(request, bookmarks=None):
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

@require_superuser
def add_url(request):
    callback = request.GET.get('callback')
    title = request.GET.get('title')
    url = request.GET.get('url')
    tags = request.GET.get('tags', '').split(',')
    metaurl = request.GET.get('metaurl', 'null').lower()
    metaurl = None if metaurl.lower() == 'null' else metaurl

    if not callback or not url:
        return HttpResponse('missing params', status=400)

    data = { 'status': 'ok' }

    try:
        bookmark = Bookmark.objects.get(url=url)
    except Bookmark.DoesNotExist:
        bookmark = Bookmark(title=title, url=url, meta_url=metaurl)
        bookmark.save()

    for tag_text in tags:
        if tag_text:
            tag, created = BookmarkTag.objects.get_or_create(text=tag_text)
            bookmark.tags.add(tag)
    bookmark.save()

    return HttpResponse('%s(%s);' % (callback,json.dumps(data),), content_type='application/javascript')
