from django.conf.urls import patterns, include, url
from Goali.views import homepage
from django.contrib.auth.views import login, logout
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', homepage),
	
	#admin-site
	url(r'^admin/', include(admin.site.urls)),
	
	#login / logout
	url(r'^login$', 'django.contrib.auth.views.login'),
	url(r'^logout$', logout),	
	
)
