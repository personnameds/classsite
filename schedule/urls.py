from django.conf.urls import patterns, include, url
from schedule.views import ScheduleTemplateView
from django.contrib.auth.decorators import permission_required
from day_no.views import UpdateDayNoView

urlpatterns = patterns('',
	url(r'^$', ScheduleTemplateView.as_view(), name='schedule_view'),
	url(r'^modify/(?P<pk>\d+)/(?P<kid>\d+)$', permission_required('classlists.is_kksastaff', login_url='/registration/login/')(UpdateDayNoView.as_view())),

	)
