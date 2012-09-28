import re

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from toolbox.models import Tag, TaggedItem


class PostTag(Tag): pass


class Post(TaggedItem, models.Model):

    class Meta(object):
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.generate_slug()

        return super(Post, self).save(*args, **kwargs)

    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User)
    content = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True,blank=True)

    is_published = models.BooleanField(default=False)

    #TaggedItem mixin
    tags = models.ManyToManyField(PostTag, blank=True)

    def generate_slug(self):
        #based on http://cubiq.org/the-perfect-php-clean-url-generator
        slug = re.sub(r'[^a-zA-Z0-9\/_|+ -]', '', self.title)
        slug = slug.strip('-').lower()
        self.slug = re.sub(r'[\/_|+ -]+', '-', slug);
        return self.slug


def set_published_date(sender, instance, raw, using, **kwargs):
    if raw: return #True if the model is saved exactly as presented (i.e. when loading a fixture)

    if instance.is_published and not instance.published_date:
        instance.published_date = instance.last_modified_date
        instance.save()
post_save.connect(set_published_date, sender=Post)
