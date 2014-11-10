from django.conf.urls import patterns, include, url
from django.contrib import admin
from chordcon import views

urlpatterns = patterns('',
    url(r'^chordconverter/', include('chordconverter.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index', include('views.index')),
)
