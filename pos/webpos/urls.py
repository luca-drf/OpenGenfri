from django.conf.urls import patterns, url
from webpos import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^refresh/$', login_required(views.refresh_buttons), name='refresh'),
    # url(r'^commit/$', views.commit_bill, name='commit'),
    url(r'^report/', login_required(views.report), name='report'),
    url(r'^bill/(?P<pk>\d+)/$', login_required(views.BillDetailView.as_view()),
        name='bill-detail'),

)
