from django.conf.urls import patterns, include, url
from Goali.views import hello, current_datetime
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', hello),
	url(r'^$', current_datetime),
)
