from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from CTF.views import register, profile, ChallengeView, ContestView, home_page


# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
  # Examples:
  # url(r'^$', 'NightShade.views.home', name='home'),
  # url(r'^NightShade/', include('NightShade.foo.urls')),
  url(r'^$', home_page, name='home_page'),
  url(r'^time/$', home_page, name='home'),

  # CTF URL Patterns
  url(r'^contests/(?P<slug>[-_\w]+)/', ContestView, name='contest-view'),
  url(r'^challenge/(?P<slug>[-_\w]+)/', ChallengeView, name='challenge-view'),

  # Login patterns
  url(r'^accounts/login/$', login, name='login'),
  url(r'^accounts/logout/$', logout, name='logout'),
  url(r'^accounts/register/$', register, name='register'),
  url(r'^accounts/profile/(?P<username>[\.-_\w]+)/', profile, name='profile'),

  # Uncomment the admin/doc line below to enable admin documentation:
  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  url(r'^admin/', include(admin.site.urls)),
)
