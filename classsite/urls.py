from django.conf.urls import patterns, include, url
from django.conf import settings #development only used to show media files
from django.conf.urls.static import static #development only used to show media files

# from django.views.generic import ListView
# from classlists.models import Classes


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

#     url(r'^$', ListView.as_view(
#                 model=Classes,
#                 context_object_name="classes_list",
#                 template_name='whichclass.html',
#                 )),
#     url(r'^add_class/', include('classlists.urls')),  
     url(r'^(?P<class_url>\w{2})/', include('homepage.urls')),
#     url(r'^(?P<class_url>\w{2})/registration/',include('registration.urls')),
#     url(r'^(?P<class_url>\w{2})/calendar/', include('kalendar.urls')),
#     url(r'^(?P<class_url>\w{2})/schedule/', include('schedule.urls')),
#     url(r'^(?P<class_url>\w{2})/homework/', include('homework.urls')),
#     url(r'^(?P<class_url>\w{2})/documents/', include('documents.urls')),
#     url(r'^(?P<class_url>\w{2})/links/', include('links.urls')),
#     url(r'^(?P<class_url>\w{2})/messages/', include('messages.urls')),
#     url(r'^(?P<class_url>\w{2})/contact/', include('contact.urls')),
# 
#     
#     url(r'^registration/login/','registration.views.unknownlogin'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #development only used to show media files
