from django.shortcuts import render, redirect
from blog.models import Post

def recent(request, posts_to_show=5):
    context = {}
    context['posts'] = Post.objects.filter(is_published=True).order_by('-created_date')[:posts_to_show]
    return render(request, 'blog/recent.html', context)
