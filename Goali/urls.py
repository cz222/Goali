from django.conf.urls import patterns, include, url
from Goali.views import homepage, login_new, logout, about, lounge, forums, forum, thread
from accounts.views import goals, osgoals, msgoals, tosgoals, tmsgoals, vgoals, pgoals, test_view
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
	#homepage
	url(r'^$', homepage, name='homepage'),
	
	#Lounge Page
	url(r'^lounge/', lounge, name='lounge'),
	
	#Forums
	url(r'forums/', forums, name='forums'),
	url(r'^forum/(\d+)/$', forum, name='forum'),
	url(r'^thread/(\d+)/$', thread, name='thread'),
	
	#Test link
	url(r'^test/$', test_view),

	#About Page
	url(r'^about/', about),
	
	#login / logout
	url(r'^login_new/', login_new, name='login_new'),
	url(r'^logout/', logout, name='logout'),	

	#One Shot Goal Pages
	url(r'^user/(?P<username>.+?)/osgoals/(?P<title>.+?)(?P<id>\d)/$', osgoals, name='osgoals'),
	
	#Milestone Goal Pages
	url(r'^user/(?P<username>.+?)/msgoals/(?P<title>.+?)(?P<id>\d)/$', msgoals, name='msgoals'),
	
	#Time One Shot Goal Pages
	url(r'^user/(?P<username>.+?)/tosgoals/(?P<title>.+?)(?P<id>\d)/$', tosgoals, name='tosgoals'),
	
	#Time Milestone Goal Pages
	url(r'^user/(?P<username>.+?)/tmsgoals/(?P<title>.+?)(?P<id>\d)/$', tmsgoals, name='tmsgoals'),
	
	#Value Goal Pages
	url(r'^user/(?P<username>.+?)/vgoals/(?P<title>.+?)(?P<id>\d)/$', vgoals, name='vgoals'),
	
	#Progress Goal Pages
	url(r'^user/(?P<username>.+?)/pgoals/(?P<title>.+?)(?P<id>\d)/$', pgoals, name='pgoals'),
	
	#Personal Goals (authorization required)
	url(r'^user/(?P<username>.+?)/$', goals, name='goals'),
	
	#admin-site
	url(r'^admin/', include(admin.site.urls)),
	
	#media
	#(r'^media/(?P<path>.*)$', 'django.views.static.serve', {document_root': settings.MEDIA_ROOT}))
)