from django.conf.urls import patterns, url

from homepage.views import HomepageListView, HomepageCreateView, HomepageUpdateView
from django.contrib.auth.decorators import permission_required


urlpatterns=patterns('',
    url(r'^$', HomepageListView.as_view(), name='homepage-list-view'),
    url(r'^add/$', permission_required('classlists.is_kksastaff', login_url='/registration/login/')(HomepageCreateView.as_view())), 
    url(r'^modify/(?P<pk>\d+)/$', permission_required('classlists.is_kksastaff', login_url='/registration/login/')(HomepageUpdateView.as_view())), 
     )