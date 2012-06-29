import re

from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    permalink = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    content = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True,blank=True)

    is_published = models.BooleanField(default=False)

    def generate_permalink(self):
        permalink = re.sub(r'[^a-zA-Z0-9\/_|+ -]', '', self.title)
        permalink = permalink.strip('-').lower()
        self.permalink = re.sub(r'[\/_|+ -]+', '-', permalink);
        return self.permalink
