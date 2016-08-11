from django.conf.urls import url
from .views import KalendarListView, DayNoUpdateView, EventCreateView, EventUpdateView, SchoolKalendarTemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$', KalendarListView.as_view(), name='kalendar-list-view'),
	url(r'^school/$', SchoolKalendarTemplateView.as_view(), name='school_kalendar-template-view'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})$', KalendarListView.as_view(), name='kalendar-view'),	#if sent with month, day etc.
    url(r'^changeday/(?P<pk>\d+)/$', DayNoUpdateView.as_view(), name='dayno-update-view'),
    url(r'^addevent/(?P<pk>\d+)/$', EventCreateView.as_view(), name='event-create-view'),
    url(r'^changeevent/(?P<pk>\d+)/$', EventUpdateView.as_view(), name='event-update-view'),
    ]
