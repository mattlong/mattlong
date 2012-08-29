import json

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils.functional import wraps

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

def require_superuser(view):
    @wraps(view)
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied()
        return view(request, *args, **kwargs)
    return _inner
