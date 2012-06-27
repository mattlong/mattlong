from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)

class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist,null=True,blank=True)
    rating = models.IntegerField(null=True,blank=True)
    source = models.CharField(max_length=30,null=True,blank=True)
    fields = models.TextField() #json
