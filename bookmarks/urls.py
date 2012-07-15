from django.conf.urls import patterns, include, url

urlpatterns = patterns('bookmarks.views',
    url(r'^$', 'all',),
    url(r'^all/$', 'all',),
    url(r'^add$', 'add_url',),
)
