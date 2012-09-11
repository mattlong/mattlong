from django.core import serializers
from django.shortcuts import render

from music import api

def index(request):
    context = {}
    songs = api.search_songs()
    context['jsonsongs'] = serializers.serialize('json', songs, ensure_ascii=False)
    return render(request, 'music/index.html', context)
