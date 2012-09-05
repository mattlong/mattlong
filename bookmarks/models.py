from django.db import models

from toolbox.models import Tag, TaggedItem

class BookmarkTag(Tag): pass

class Bookmark(TaggedItem, models.Model):
    title = models.CharField(max_length=200)
    url = models.TextField(unique=True)
    meta_url = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=10, default='NEW')
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    #TaggedItem mixin
    tags = models.ManyToManyField(BookmarkTag)
