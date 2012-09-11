from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('blog.urls')),

    url(r'^posts/', include('blog.urls')),

    url(r'^bookmarks/', include('bookmarks.urls')),

    url(r'^music/', include('music.urls')),
    url(r'^api/music', include('music.api_urls')),

    url(r'^projects/$', 'django.views.generic.simple.direct_to_template', {'template': 'projects.html'},),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'toolbox.views.oauth_login'),
    url(r'^oauth2callback$', 'toolbox.views.oauth_callback'),
)
