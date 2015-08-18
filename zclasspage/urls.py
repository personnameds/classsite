from django.conf.urls import patterns, url

from classpage.views import ClasspageListView, ClasspageCreateView, ClasspageUpdateView
from django.contrib.auth.decorators import permission_required


urlpatterns=patterns('',
    url(r'^$', ClasspageListView.as_view(), name='classpage-list-view'),
    url(r'^add/$', permission_required('classlists.is_kksastaff', login_url='/registration/login/')(ClasspageCreateView.as_view())), 
    url(r'^modify/(?P<pk>\d+)/$', permission_required('classlists.is_kksastaff', login_url='/registration/login/')(ClasspageUpdateView.as_view())), 
     )