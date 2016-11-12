from django.conf.urls import patterns, url
from django.conf import settings


urlpatterns = patterns(
    '',
    url(r'^$', 'web.views.home', name="home"),
    url(r'^login$', 'web.views.login', name="login"),
    url(r'^register$', 'web.views.register', name="register"),

    # Outputs
    url(r'^search-output$', 'web.views.search_output', name="search-output"),
    url(r'^add-output$', 'web.views.add_output', name="add-output"),
    url(r'^add-output/(?P<txid>[0-9A-Z-a-z]+)/(?P<network>[a-z]+)$', 
    	'web.views.add_output', name="add-output"),
)
