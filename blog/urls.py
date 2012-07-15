from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
    url(r'^$', 'recent',),
    url(r'^all/$', 'all',),
    url(r'^(?P<permalink>[\w\-]+)', 'single',),
)
