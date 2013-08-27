from django.conf.urls.defaults import patterns, include, url
from kalendar.views import KalendarListView,UpdateDayNoKalendarView, EventCreateView, EventUpdateView 
#from django.contrib.auth.decorators import permission_required, user_passes_test

urlpatterns = patterns('',
    #kalendar urls
 	url(r'^(?P<kal_type>\w{4,5})/$', KalendarListView.as_view()), #if sent without month, day etc.
    url(r'^(?P<kal_type>\w{4,5})/(?P<year>\d{4})/(?P<month>\d{1,2})$', KalendarListView.as_view(), name='kalendar_view'),	#if sent with month, day etc.	
    url(r'^(?P<kal_type>\w{4,5})/modify/(?P<pk>\d+)/$', UpdateDayNoKalendarView.as_view()), #modifies kalendar day nos #needs security
 	
 	#event urls
    url(r'^(?P<kal_type>\w{4,5})/add_event/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})$',EventCreateView.as_view()), ##adds events to calendar
    url(r'^(?P<kal_type>\w{4,5})/modify_event/(?P<pk>\d+)/$',EventUpdateView.as_view()), ##modify events to calendar

	)