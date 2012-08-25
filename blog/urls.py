from django.conf.urls import patterns, include, url

from blog.views import PostDetailView, PostSummaryView, PostListView

urlpatterns = patterns('blog.views',
    url(r'^$', PostListView.as_view()),
    url(r'^all/$', PostSummaryView.as_view()),
    url(r'^(?P<slug>[\w\-]+)/$', PostDetailView.as_view()),
)
