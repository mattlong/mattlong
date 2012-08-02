from django.contrib import admin
from bookmarks.models import Bookmark, BookmarkTag

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
admin.site.register(Bookmark, BookmarkAdmin)

class BookmarkTagAdmin(admin.ModelAdmin):
    list_display = ('text',)
admin.site.register(BookmarkTag, BookmarkTagAdmin)

