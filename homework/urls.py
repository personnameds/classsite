from django.conf.urls.defaults import patterns, include, url
from homework.models import Homework
from homework.views import HomeworkListView, HomeworkCreateView, HomeworkUpdateView
from django.contrib.auth.decorators import login_required
#from classsite3.feed import HomeworkEntriesFeed

from datetime import date

urlpatterns = patterns('',
	url(r'^$', HomeworkListView.as_view(), name='homework-list-view'),
	url(r'^add/$',login_required(HomeworkCreateView.as_view())),
	url(r'^modify/(?P<pk>\d+)/$',login_required(HomeworkUpdateView.as_view())),
	#url(r'^feed/$',HomeworkEntriesFeed()),
 											
	)
