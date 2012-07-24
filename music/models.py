from django.db import models

import toolbox

class Artist(models.Model):
    name = models.CharField(max_length=100)

class SongTag(toolbox.models.Tag): pass

class Song(toolbox.models.TaggedItem, models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist,null=True,blank=True)
    rating = models.IntegerField(null=True,blank=True)
    source = models.CharField(max_length=30,null=True,blank=True)
    fields = models.TextField() #json

    #TaggedItem mixin
    tags = models.ManyToManyField(SongTag)
