from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.conf.urls.static import static
import os.path

#from ticket1.views import my_homepage_view
from ticket1 import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
#admin.autodiscover()


admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
     #url(r'^$', 'tickets.views.home', name='home'),
     #url(r'^tickets/', include('tickets.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

     url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT, 'show_indexes': True}),
     
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     #url(r'^$', views.my_homepage_view),
     url(r'^$', views.ticket1_main_query),
     url(r'^search_sample/$', views.search_sample),
     url(r'^search/$', views.search),
     url(r'^accounts/login/$', login),
     url(r'^accounts/logout/$', logout),
     url(r'^accounts/register/$', views.register),
     url(r'^order/$', views.ticket1_order),
     url(r'^order_submit/$', views.ticket1_order_submit),
     url(r'^order_quote/$', views.ticket1_order_quote),
     url(r'^order_query/$', views.ticket1_order_query),
     url(r'^order_delete/$', views.ticket1_order_delete),
)
