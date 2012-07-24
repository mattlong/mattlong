import re

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save

import toolbox

class PostTag(toolbox.models.Tag): pass

class Post(toolbox.models.TaggedItem, models.Model):
    title = models.CharField(max_length=100)
    permalink = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User)
    content = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True,blank=True)

    is_published = models.BooleanField(default=False)

    #TaggedItem mixin
    tags = models.ManyToManyField(PostTag)

    def generate_permalink(self):
        #based on http://cubiq.org/the-perfect-php-clean-url-generator
        permalink = re.sub(r'[^a-zA-Z0-9\/_|+ -]', '', self.title)
        permalink = permalink.strip('-').lower()
        self.permalink = re.sub(r'[\/_|+ -]+', '-', permalink);
        return self.permalink

def add_permalink(sender, instance, raw, using, **kwargs):
    if raw: return

    if not instance.permalink:
        instance.generate_permalink()
pre_save.connect(add_permalink, sender=Post)
