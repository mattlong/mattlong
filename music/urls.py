from django.conf.urls import patterns, include, url

urlpatterns = patterns('music',
    url(r'^$', 'views.index'),
)
