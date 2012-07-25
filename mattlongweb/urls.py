from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', include('blog.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^projects/$', 'direct_to_template', {'template': 'projects.html'},),

    url(r'^posts/', include('blog.urls')),
    url(r'^bookmarks/', include('bookmarks.urls')),
    url(r'^music/', include('music.urls')),
)
