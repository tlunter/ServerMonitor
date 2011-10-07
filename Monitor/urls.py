from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('Monitor.views',
    url(r'^server/edit/(?P<id>\d+)/$','edit_server',name='edit-server'),
    url(r'^login/$','login',name='login'),
    url(r'^logout/$','logout',name='logout'),
    url(r'^$','main',name='main_page'),
)
