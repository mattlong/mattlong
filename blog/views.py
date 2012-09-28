from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from toolbox import require_superuser

from blog.models import Post

class PostSummaryView(ListView):
    model = Post
    paginate_by = 20
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(is_published=True)[:self.paginate_by]
        return queryset


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_detail.html'
    paginate_by = 10
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(is_published=True)[:self.paginate_by]
        return queryset


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['object_list'] = (self.object,)
        return context


class PostCreateView(CreateView):
    model = Post
    success_url="/posts/%(slug)s/"

class PostUpdateView(UpdateView):
    model = Post
    success_url="/posts/%(slug)s/"

@require_superuser
def edit_post(request, slug=None):
    initial = {}

    if slug is None:
        view_class = PostCreateView
        initial['author'] = request.user
    else:
        view_class = PostUpdateView

    return view_class.as_view(initial=initial)(request, slug=slug)
