from django.conf.urls.defaults import patterns, include, url
from links.views import LinkListView, LinkCreateView, LinkUpdateView
from django.contrib.auth.decorators import user_passes_test
urlpatterns = patterns('',
	url(r'^$', LinkListView.as_view(), name='link-list-view'),
 	url(r'^add/$',user_passes_test(lambda u:u.is_staff)(LinkCreateView.as_view())),
 	url(r'^modify/(?P<pk>\d+)/$', user_passes_test(lambda u:u.is_staff)(LinkUpdateView.as_view())),									
	)