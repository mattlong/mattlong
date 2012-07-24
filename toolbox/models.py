from django.db import models

#mixin
class TaggedItem(object):
    def get_tags(self):
        return self.tags.all()

#abstract model
class TagRelation(models.Model):
    class Meta(object):
        abstract = True

    tagged_date = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    class Meta(object):
        abstract = True

    text = models.CharField(max_length=30,unique=True)
