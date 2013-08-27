from django.conf.urls.defaults import patterns, include, url
from links.views import LinkListView, LinkCreateView, LinkUpdateView
#from django.contrib.auth.decorators import user_passes_test

urlpatterns = patterns('',
	url(r'^$', LinkListView.as_view(), name='link_view'),
 	url(r'^add/$',LinkCreateView.as_view()),
 	url(r'^modify/(?P<pk>\d+)/$', LinkUpdateView.as_view()),									
	)