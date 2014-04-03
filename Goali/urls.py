from django.conf.urls import patterns, include, url
from Goali.views import homepage
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	url(r'^$', homepage),
	
	#login / logout
	url(r'^login$', 'django.contrib.auth.views.login'),
	url(r'^logout$', logout),	
	
)
