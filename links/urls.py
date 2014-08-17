from django.conf.urls import patterns, include, url
from links.views import LinkListView, LinkCreateView, LinkUpdateView
from django.contrib.auth.decorators import permission_required

urlpatterns = patterns('',
	url(r'^$', LinkListView.as_view(), name='link_view'),
 	url(r'^add/$',permission_required('classlists.is_kksastaff', login_url='/registration/login/')(LinkCreateView.as_view())),
 	url(r'^modify/(?P<pk>\d+)/$', permission_required('classlists.is_kksastaff', login_url='/registration/login/')(LinkUpdateView.as_view())),									
	)