from django.conf.urls import patterns, url
from .views import HomeworkListView, HomeworkCreateView, HomeworkUpdateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
	url(r'^$', HomeworkListView.as_view(), name='homework-list-view'),
	url(r'^add/$',login_required()(HomeworkCreateView.as_view()), name='homework-create-view'),
	url(r'^modify/(?P<pk>\d+)/$',login_required()(HomeworkUpdateView.as_view()), name='homework-update-view'),
	)
