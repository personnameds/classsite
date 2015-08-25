from django.conf.urls import patterns, url

from .views import SchoolpageListView

##TO DO Permissions
urlpatterns = [
	url(r'^$', SchoolpageListView.as_view(), name='schoolpage-list-view'),
]


#     url(r'^add/$', permission_required('classlists.is_kksastaff', login_url='/registration/login/')(SchoolpageCreateView.as_view())), 
#     url(r'^modify/(?P<pk>\d+)/$', permission_required('classlists.is_kksastaff', login_url='/registration/login/')(SchoolpageUpdateView.as_view())), 
#      )