from django.conf.urls import patterns, include, url

urlpatterns = patterns('music',
    url(r'^$', 'views.index'),

    url(r'^find$', 'views.find'),

    #url(r'^$', 'direct_to_template', {'template': 'index.html'},),
)
