from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^webpos/', include('webpos.urls', namespace="webpos")),
    url(r'^admin/', include(admin.site.urls)),
)
