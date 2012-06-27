from django.shortcuts import render, redirect
from blog.models import Post

def recent(request):
    context = {}
    context['posts'] = Post.objects.order_by('-created_date')[:5]
    return render(request, 'blog/recent.html', context)
