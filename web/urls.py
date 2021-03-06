from django.conf.urls import patterns, url
from django.conf import settings


urlpatterns = patterns(
    '',
    url(r'^$', 'web.views.home', name="home"),
    url(r'^accounts/logout/$', 'web.views.logout', name="logout"),
    url(r'^accounts/login/$', 'web.views.login', name="login"),
    url(r'^accounts/register/$', 'web.views.register', name="register"),

    # Outputs
    url(r'^search-output/$', 'web.views.search_output', name="search-output"),
    url(r'^add-output/$', 'web.views.add_output', name="add-output"),
    url(r'^following-outputs/$', 'web.views.following_outputs', name="following-outputs"),
	url(r'^cancel-output/(?P<following_id>[0-9]+)/$', 'web.views.cancel_output', name="cancel-output"),
    url(r'^confirm-output/(?P<following_id>[0-9]+)/$', 'web.views.confirm_output', name="confirm-output"),
)
