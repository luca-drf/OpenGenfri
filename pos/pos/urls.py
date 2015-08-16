from pos import views
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_change
from django.views.generic.base import RedirectView, TemplateView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='webpos/'), name='index'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^chpwd/$', password_change, {'template_name': 'change_pass.html',
                                       'post_change_redirect': 'success/'},
                                      name='chpwd'),
    url(r'^chpwd/success/$', TemplateView.as_view(template_name='success.html')),
    url(r'^webpos/', include('webpos.urls', namespace="webpos")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^check/$', views.check, name='check'),
)
