from django.conf.urls.defaults import patterns, include, url
from homework.models import Homework
from homework.views import HomeworkListView, HomeworkCreateView, HomeworkUpdateView
from django.contrib.auth.decorators import login_required
#from classsite3.feed import HomeworkEntriesFeed

from datetime import date

urlpatterns = patterns('',
	url(r'^$', HomeworkListView.as_view(), name='homework_view'),
	url(r'^add/$',login_required(login_url='/registration/login/')(HomeworkCreateView.as_view())),
	url(r'^modify/(?P<pk>\d+)/$',login_required(login_url='/registration/login/')(HomeworkUpdateView.as_view())),
	#url(r'^feed/$',HomeworkEntriesFeed()),
 											
	)
