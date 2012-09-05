import json

from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from toolbox import JsonResponse, require_superuser

from music.models import Song

def search_songs(query=None, order_by='-id'):
    if not query:
        songs = Song.objects.order_by(order_by)[:100]
    else:
        name_q = Q(name__contains=query)
        artist_q = Q(artist__name__contains=query)
        tag_q = Q(tags__text=query)
        songs = Song.objects.filter(name_q | artist_q | tag_q).order_by(order_by)
    return songs

def index(request):
    context = {}
    songs = search_songs()
    context['jsonsongs'] = serializers.serialize('json', songs, ensure_ascii=False)
    return render(request, 'music/index.html', context)

def find(request):
    query = request.GET.get('q', '')

    songs = search_songs(query=query)

    return JsonResponse(songs)
