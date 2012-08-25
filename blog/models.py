import re

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save

from toolbox.models import Tag, TaggedItem

class PostTag(Tag): pass

class Post(TaggedItem, models.Model):

    class Meta(object):
        ordering = ['-published_date']

    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User)
    content = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True,blank=True)

    is_published = models.BooleanField(default=False)

    #TaggedItem mixin
    tags = models.ManyToManyField(PostTag)

    def generate_slug(self):
        #based on http://cubiq.org/the-perfect-php-clean-url-generator
        slug = re.sub(r'[^a-zA-Z0-9\/_|+ -]', '', self.title)
        slug = slug.strip('-').lower()
        self.slug = re.sub(r'[\/_|+ -]+', '-', slug);
        return self.slug

def add_slug(sender, instance, raw, using, **kwargs):
    if raw: return #True if the model is saved exactly as presented (i.e. when loading a fixture)

    if not instance.slug:
        instance.generate_slug()
pre_save.connect(add_slug, sender=Post)
