from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from .views import SchoolpageListView, SchoolpageCreateView, SchoolpageUpdateView

##TO DO Permissions
urlpatterns = [
	url(r'^$', SchoolpageListView.as_view(), name='schoolpage-list-view'),
	url(r'^add/$', permission_required('schoolpage.add_schoolpage')(SchoolpageCreateView.as_view()), name='schoolpage-create-view'),
	url(r'^modify/(?P<pk>\d+)/$', permission_required('schoolpage.change_schoolpage')(SchoolpageUpdateView.as_view()), name='schoolpage-update-view'),
]
