from django.conf.urls.defaults import patterns, include, url
from schedule.views import ScheduleTemplateView
from django.contrib.auth.decorators import user_passes_test
from day_no.views import UpdateDayNoView

urlpatterns = patterns('',
	url(r'^$', ScheduleTemplateView.as_view(), name='schedule-template-view'),
	url(r'^modify/(?P<pk>\d+)/(?P<kid>\d+)$',user_passes_test(lambda u:u.is_staff)(UpdateDayNoView.as_view())),

	)
