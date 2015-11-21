from django.conf.urls import patterns, url
from .views import ScheduleView, ActivityCreateView, ActivityUpdateView ##, ActivityDayUpdateView
from django.contrib.auth.decorators import permission_required

urlpatterns = patterns('',
	url(r'^$', ScheduleView.as_view(), name='schedule-view'),
	url(r'^addactivity/(?P<perdet_pk>\d+)/(?P<dayno_pk>\d+)/$', permission_required('schedule.add_period_activity')(ActivityCreateView.as_view()), name='activity-create-view'),
	url(r'^updateactivity/(?P<perdet_pk>\d+)/(?P<pk>\d+)/$', permission_required('schedule.change_period_activity')(ActivityUpdateView.as_view()), name='activity-update-view'),
##	url(r'^dayupdate/(?P<dayno_pk>\d+)/$', permission_required('schedule.change_period_activity')(ActivityDayUpdateView.as_view()), name='activity-day-update'),

    )
    