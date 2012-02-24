from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('Monitor.views',
    url(r'^messages/edit/(?P<id>\d+)/$','edit_message',name='edit-message'),
    url(r'^messages/(?P<id>\d+)/$','view_messages',name='view-messages'),
    url(r'^add-server/$','add_server',name='add-server'),
    url(r'^server/(?P<id>\d+)/edit/$','edit_server',name='edit-server'),
    url(r'^monitors/(?P<id>\d+)/$','view_monitors',name='view-monitors'),
    url(r'^login/$','login',name='login'),
    url(r'^logout/$','logout',name='logout'),
    url(r'^$','main',name='main_page'),
)
