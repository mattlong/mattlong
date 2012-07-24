from django.db import models

import toolbox

class BookmarkTag(toolbox.models.Tag): pass

class Bookmark(toolbox.models.TaggedItem, models.Model):
    title = models.CharField(max_length=200)
    url = models.TextField(unique=True)
    meta_url = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=10, default='NEW')
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    #TaggedItem mixin
    tags = models.ManyToManyField(BookmarkTag)
