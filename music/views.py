import json

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'music/index.html', context)

def find(request):
    query = request.GET['q']
    return HttpResponse(json.dumps(query))
