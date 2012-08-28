from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from blog.models import Post

class PostSummaryView(ListView):
    model = Post
    paginate_by = 20

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_detail.html'
    paginate_by = 2
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
