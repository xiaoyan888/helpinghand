from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView

#class MyRegistrationView(RegistrationView):
#    def get_success_url(self, request, user):
#        return '/rango/'
#class MyRegistrationView(RegistrationView):
 #   def get_success_url(self,request, user):
  #      return '/rango/'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'helpinghand.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
#url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
   # url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),# new app tuple the code
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
                            (r'^media/(?P<path>.*)',
                             'serve',
                             {'document_root': settings.MEDIA_ROOT}),)
