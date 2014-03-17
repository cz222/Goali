from django.conf.urls import patterns, include, url
from Goali.views import hello, current_datetime
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    #url(r'^$', hello),
	url(r'^$', current_datetime),
	url(r'^login$', login, {'template_name': 'account.html'}, name='auth_login'),
	url(r'^logout$', logout, {'template_name': 'logout.html'}, name='auth_logout'),	
)
