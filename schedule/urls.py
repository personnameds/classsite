from django.conf.urls.defaults import patterns, include, url
from schedule.views import ScheduleTemplateView
#from django.contrib.auth.decorators import user_passes_test
from day_no.views import UpdateDayNoView

urlpatterns = patterns('',
	url(r'^$', ScheduleTemplateView.as_view(), name='schedule_view'),
	url(r'^modify/(?P<pk>\d+)/(?P<kid>\d+)$', UpdateDayNoView.as_view()),

	)
