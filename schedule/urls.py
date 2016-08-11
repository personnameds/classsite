from django.conf.urls import url
from .views import ScheduleView, ActivityUpdateView, ActivityDayUpdateView
from django.contrib.auth.decorators import permission_required

urlpatterns = [
	url(r'^$', ScheduleView.as_view(), name='schedule-view'),
	url(r'^updateactivity/(?P<perdet_pk>\w+)/(?P<pk>\w+)/$', permission_required('schedule.change_period_activity')(ActivityUpdateView.as_view()), name='activity-update-view'),
	url(r'^dayupdate/(?P<dayno_pk>\w+)/$', permission_required('schedule.change_period_activity')(ActivityDayUpdateView.as_view()), name='activity-day-update'),

    ]
    