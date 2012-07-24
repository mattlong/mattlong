from django.contrib import admin
from music.models import Song, SongTag, Artist

class SongTagAdmin(admin.ModelAdmin):
    list_display = ('text',)
admin.site.register(SongTag, SongTagAdmin)

class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'source')
admin.site.register(Song, SongAdmin)

