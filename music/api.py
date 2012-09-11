import json

from django.db.models import Q
from django.core import serializers

from toolbox import JsonResponse, require_superuser

from music.models import Song, Artist

def search_songs(query=None, order_by='-id'):
    if not query:
        songs = Song.objects.order_by(order_by)[:100]
    else:
        name_q = Q(name__contains=query)
        artist_q = Q(artist__name__contains=query)
        tag_q = Q(tags__text=query)
        songs = Song.objects.filter(name_q | artist_q | tag_q).order_by(order_by)
    return songs

def base(request):
    if request.method == 'GET':
        return base_get(request)
    elif request.method == 'POST':
        return base_post(request)

def base_get(request):
    query = request.GET.get('q', '')

    songs = search_songs(query=query)

    return JsonResponse(songs)

@require_superuser
def base_post(request):
    print request.body
    params = json.loads(request.body)
    title = params.get('title')
    artist = params.get('artist')
    source = params.get('source')

    if not title:
        return JsonResponse({'error': 'missing title'}, status=400)

    song = Song.objects.filter(name=title)

    if artist:
        song = song.filter(artist__name__contains=artist)

    if len(song) > 0:
        return JsonResponse({'error': 'song exists'}, status=400)

    (artist, _) = Artist.objects.get_or_create(name=artist)
    song = Song.objects.create(name=title, artist=artist, source=source)

    return JsonResponse()
