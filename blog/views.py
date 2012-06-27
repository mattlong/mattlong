from django.http import Http404
from django.shortcuts import render, redirect

from blog.models import Post

def all(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_date')
    return list_posts(request, posts=posts)

def recent(request, posts_to_show=5):
    posts = Post.objects.filter(is_published=True).order_by('-created_date')[:posts_to_show]
    return detail_posts(request, posts=posts)

def single(request, url_title=None):
    if not url_title: raise Http404()

    try:
        post = Post.objects.get(url_title=url_title.lower())
    except:
        raise

    return detail_posts(request, posts=(post,))

def list_posts(request, posts=None):
    if not posts: raise Http404()

    context = {}
    context['posts'] = posts
    return render(request, 'blog/list.html', context)

def detail_posts(request, posts=None):
    if not posts: raise Http404()

    context = {}
    context['posts'] = posts
    return render(request, 'blog/detail.html', context)
