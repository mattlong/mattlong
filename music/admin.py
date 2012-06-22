from django.contrib import admin
from music.models import Song, Artist

class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'source')
admin.site.register(Song, SongAdmin)

