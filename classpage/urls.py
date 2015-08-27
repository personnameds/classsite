from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required
from .views import ClasspageListView, ClasspageCreateView

urlpatterns = [
    url(r'^$', ClasspageListView.as_view(), name='classpage-list-view'),
    url(r'^(?i)add/$', permission_required('classpage.add_classpage')(ClasspageCreateView.as_view()), name='classpage-create-view'),
]



# from django.conf.urls import patterns, url
# 
# from classpage.views import ClasspageListView, ClasspageCreateView, ClasspageUpdateView
# from django.contrib.auth.decorators import permission_required
# 
# 
# urlpatterns=patterns('',
#     url(r'^$', ClasspageListView.as_view(), name='classpage-list-view'),
#     url(r'^add/$', permission_required('classlists.is_kksastaff', login_url='/registration/login/')(ClasspageCreateView.as_view())), 
#     url(r'^modify/(?P<pk>\d+)/$', permission_required('classlists.is_kksastaff', login_url='/registration/login/')(ClasspageUpdateView.as_view())), 
#      )


# 
# urlpatterns = [
# 	url(r'^$', SchoolpageListView.as_view(), name='schoolpage-list-view'),
# 	url(r'^add/$', permission_required('schoolpage.add_schoolpage')(SchoolpageCreateView.as_view()), name='schoolpage-create-view'),
# 	url(r'^modify/(?P<pk>\d+)/$', permission_required('schoolpage.change_schoolpage')(SchoolpageUpdateView.as_view()), name='schoolpage-update-view'),
# ]
