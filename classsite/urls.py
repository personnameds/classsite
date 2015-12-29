from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout, login

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('schoolpage.urls')),
#    url(r'^oauth2callback', 'kalendar.views.auth_return'),
    url(r'^(?i)(?P<class_url>[a-z0-9_-]{1,4})/', include('classpage.urls')),  
    url(r'^(?i)(?P<class_url>[a-z0-9_-]{1,4})/homework/', include('homework.urls')),   
    url(r'^(?i)(?P<class_url>[a-z0-9_-]{1,4})/calendar/', include('kalendar.urls')),  
    url(r'^(?i)(?P<class_url>[a-z0-9_-]{1,4})/schedule/', include('schedule.urls')),
    url(r'^(?i)(?P<class_url>[a-z0-9_-]{1,4})/documents/', include('documents.urls')),
    url(r'^(?i)(?P<class_url>[a-z0-9_-]{1,4})/links/', include('links.urls')),
    url(r'^(?i)(?P<class_url>[a-z0-9_-]{1,4})/messages/', include('msgs.urls')),
    url(r'^(?i)(?P<class_url>[a-z0-9_-]{1,4})/contact/', include('contact.urls')),
    url(r'^(?i)(?P<class_url>[a-z0-9_-]{1,4})/classlist/', include('classlists.urls')),
    url(r'^(?i)registration/', include('registration.urls')),
	url(r'^(?i)setup/', include('schoolsetup.urls')),
    url(r'^(?i)logout/$', logout,kwargs={'next_page':'/'},name='logout-view'),   
    url(r'^(?i)login/$', login,{'extra_context':{'reg_status':settings.REGISTRATION_STATUS},'template_name':'registration/login.html'},name='login-view'),    
    url(r'^(?i)admin/', include(admin.site.urls)),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

