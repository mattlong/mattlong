from django.db import models

from toolbox.models import Tag, TaggedItem

class Artist(models.Model):
    name = models.CharField(max_length=100)

class SongTag(Tag): pass

class Song(TaggedItem, models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist,null=True,blank=True)
    rating = models.IntegerField(null=True,blank=True)
    source = models.CharField(max_length=30,null=True,blank=True)
    fields = models.TextField(null=True,blank=True) #json

    #TaggedItem mixin
    tags = models.ManyToManyField(SongTag, blank=True)
