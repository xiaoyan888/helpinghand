from django.conf.urls import patterns, url
from rango import views  #, about
#from rango import about

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'), #homepage launching
                       url(r'^about', views.about, name='about'),#user click on about ...

                       url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
                       url(r'^add_category/$', views.add_category, name='add_category'),#user click on
                       url(r'^category/(?P<category_name_slug>\w+)/add_page/$', views.add_page, name='add_page'),
                       url(r'^restricted/$', views.restricted, name='restricted'),
                       url(r'^search/$', views.search, name='search'),
                       url(r'^goto/$', views.track_url, name='goto'),
                       url(r'^like_category/$', views.like_category, name='like_category'),
                       url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),) # to the next link



# url(r'^add_page/$', views.add_page, name='add_page'),
 #url(r'^logout/$', views.user_logout, name='logout'),
                       #url(r'^register/$', views.register, name='register'),
                       #url(r'^login/$', views.user_login, name='login'),