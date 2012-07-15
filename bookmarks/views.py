import json

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from bookmarks.models import Bookmark

def all(request, status='NEW'):
    bookmarks = Bookmark.objects.filter(status='NEW').order_by('-created_date')
    return list_bookmarks(request, bookmarks=bookmarks)

def list_bookmarks(request, bookmarks=None):
    if not bookmarks: raise Http404()

    for b in bookmarks:
        print b.url, type(b.meta_url), b.meta_url

    context = {}
    context['bookmarks'] = bookmarks
    return render(request, 'bookmarks/list.html', context)

def add_url(request):
    callback = request.GET['callback']
    title = request.GET.get('title')
    url = request.GET.get('url')
    metaurl = request.GET.get('metaurl', u'null').lower()
    metaurl = None if metaurl.lower() == u'null' else metaurl

    data = { 'status': 'ok' }

    try:
        bookmark = Bookmark.objects.get(url=url)
        data['exists'] = True
        return HttpResponse('%s(%s);' % (callback, json.dumps(data),))
    except Bookmark.DoesNotExist:
        pass

    bookmark = Bookmark(title=title, url=url, meta_url=metaurl)
    bookmark.save()

    return HttpResponse('%s(%s);' % (callback,json.dumps(data),));
