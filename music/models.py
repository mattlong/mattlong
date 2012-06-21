from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Artist(models.Model):
    name = models.CharField(max_length=100)

class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist,null=True,blank=True)
    rating = models.IntegerField(null=True,blank=True)
    source = models.CharField(max_length=30,null=True,blank=True)
    fields = models.TextField() #json

class UserProfile(models.Model):
    user = models.OneToOneField(User)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)
