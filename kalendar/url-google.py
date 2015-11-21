from django.conf.urls import patterns, url
#from .views import KalendarListView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
	#url(r'^$', KalendarListView.as_view(), name='kalendar-list-view'),
	url(r'^$', 'kalendar.views.index',name='kalendar-list-view'),
	)
