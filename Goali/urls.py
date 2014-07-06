from django.conf.urls import patterns, include, url
from Goali.views import homepage, login_new, logout
from accounts.views import myprofile, osgoals, msgoals, test_view
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
	#homepage
	url(r'^$', homepage, name='homepage'),
	
	#Test link
	url(r'^test/$', test_view),
	
	#login / logout
	url(r'^login_new/', login_new, name='login_new'),
	url(r'^logout/', logout, name='logout'),	

	#One Shot Goal Pages
	url(r'^user/(?P<username>.+?)/osgoals/(?P<title>.+?)(?P<id>\d)/$', osgoals, name='osgoals'),
	
	#Milestone Goal Pages
	url(r'^user/(?P<username>.+?)/msgoals/(?P<title>.+?)(?P<id>\d)/$', msgoals, name='msgoals'),
	
	#Personal Profile (authorization required)
	url(r'^user/(?P<username>.+?)/$', myprofile, name='myprofile'),
	
	#admin-site
	url(r'^admin/', include(admin.site.urls)),
	
	#media
	#(r'^media/(?P<path>.*)$', 'django.views.static.serve', {document_root': settings.MEDIA_ROOT}))
)