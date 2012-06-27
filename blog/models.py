from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    url_title = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    content = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True,blank=True)

    is_published = models.BooleanField(default=False)
