from django.conf.urls import patterns, url
from webpos import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^order/$', views.order, name='order'),
    url(r'^refresh/$', views.refresh_buttons, name='refresh'),
    # url(r'^commit/$', views.commit_bill, name='commit'),
)
