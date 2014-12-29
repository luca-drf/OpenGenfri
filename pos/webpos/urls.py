from django.conf.urls import patterns, url
from webpos import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^refresh/$', views.refresh_quantities, name='refresh'),
)
