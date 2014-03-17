from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	url(r'^login$', login, {'template_name': 'register.html'}, name='auth_login'),
	url(r'^logout$', logout, {'template_name': 'logout.html'}, name='auth_logout'),	
)