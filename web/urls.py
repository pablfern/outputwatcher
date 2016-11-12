from django.conf.urls import patterns, url
from django.conf import settings


urlpatterns = patterns(
    '',
    url(r'^$', 'web.views.home', name="home"),
    url(r'^login$', 'web.views.login', name="login"),
    url(r'^register$', 'web.views.register', name="register"),
)
