from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('schoolpage.urls')),

    url(r'^(?i)(?P<class_url>[a-z0-9_-]{1,4})/', include('classpage.urls')),    

    url(r'^(?i)logout/$', 'django.contrib.auth.views.logout',kwargs={'next_page':'/'}),   
    url(r'^(?i)login/$', 'django.contrib.auth.views.login',{'template_name':'accounts/login.html'}),    
    url(r'^(?i)admin/', include(admin.site.urls)),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

