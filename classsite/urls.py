from django.conf.urls import patterns, include, url
from django.conf import settings #development only used to show media files
from django.conf.urls.static import static #development only used to show media files

from django.views.generic import ListView
from classlists.models import Klass


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', ListView.as_view(
                queryset=Klass.objects.order_by('klass_name'),
                context_object_name="klass_list",
                template_name='index.html',
                )),
    url(r'^initialize/',include('initialize.urls')),
    url(r'^(?P<class_url>\w{2})/', include('homepage.urls')),
    url(r'^(?P<class_url>\w{2})/registration/',include('registration.urls')),
    url(r'^(?P<class_url>\w{2})/calendar/', include('kalendar.urls')),
    url(r'^(?P<class_url>\w{2})/schedule/', include('schedule.urls')),
    url(r'^(?P<class_url>\w{2})/homework/', include('homework.urls')),
    url(r'^(?P<class_url>\w{2})/documents/', include('documents.urls')),
    url(r'^(?P<class_url>\w{2})/links/', include('links.urls')),
    url(r'^(?P<class_url>\w{2})/messages/', include('messages.urls')),
    url(r'^(?P<class_url>\w{2})/contact/', include('contact.urls')),

    url(r'^registration/',include('registration.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #development only used to show media files
