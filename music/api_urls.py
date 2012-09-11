from django.conf.urls import patterns, include, url

urlpatterns = patterns('music',
    url(r'^$', 'api.base'),
    #url(r'^find$', 'views.find'),
    #url(r'^add$', 'views.add'),

    #url(r'^$', 'direct_to_template', {'template': 'index.html'},),
)
