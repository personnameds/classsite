from django.conf.urls import patterns, url
from .views import KalendarListView, DayNoUpdateView, EventCreateView, EventUpdateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
	url(r'^$', KalendarListView.as_view(), name='kalendar-list-view'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})$', KalendarListView.as_view(), name='kalendar-view'),	#if sent with month, day etc.
    url(r'^changeday/(?P<pk>\d+)/$', DayNoUpdateView.as_view(), name='dayno-update-view'),
    url(r'^addevent/(?P<pk>\d+)/$', EventCreateView.as_view(), name='event-create-view'),
    url(r'^changeevent/(?P<pk>\d+)/$', EventUpdateView.as_view(), name='event-update-view'),
    )
