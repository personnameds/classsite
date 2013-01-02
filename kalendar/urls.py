from django.conf.urls.defaults import patterns, include, url
from kalendar.views import CreateKalendarFormView, UpdateDayNoKalendarView, EventCreateView, EventUpdateView, KalendarListView
from django.contrib.auth.decorators import permission_required, user_passes_test

urlpatterns = patterns('',

 	url(r'^create_calendar/$',permission_required('kalendar.add_kalendar')(CreateKalendarFormView.as_view())),
 	url(r'^$', KalendarListView.as_view()), #if sent with no month, day etc.
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', KalendarListView.as_view(), name='kal-list-view'),	#if sent with month, day etc.
 	url(r'add_event/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})$',user_passes_test(lambda u:u.is_staff)(EventCreateView.as_view())), ##adds events to calendar
 	url(r'modify_event/(?P<pk>\d+)/$',user_passes_test(lambda u:u.is_staff)(EventUpdateView.as_view())), ##modify events to calendar
    url(r'^modify/(?P<pk>\d+)/$',permission_required('kalendar.change_kalendar')(UpdateDayNoKalendarView.as_view())), ##modifies kalendar day nos

	)