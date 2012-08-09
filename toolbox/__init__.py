import json

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.http import HttpResponse

class JsonResponse(HttpResponse):
    def __init__(self, content='', **kwargs):
        kwargs['content_type'] = 'application/json'

        if isinstance(content, basestring):
            pass
        elif isinstance(content, QuerySet):
            content = serializers.serialize('json', content, ensure_ascii=False)
        else:
            content = json.dumps(content)

        super(JsonResponse, self).__init__(content=content, **kwargs)
