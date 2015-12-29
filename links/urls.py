from django.conf.urls import url
from .views import LinkListView, LinkCreateView, LinkUpdateView
from django.contrib.auth.decorators import permission_required

urlpatterns = [
	url(r'^$', LinkListView.as_view(), name='link-list-view'),
 	url(r'^add/$',permission_required('links.add_link')(LinkCreateView.as_view()),name='link-create-view'),
	url(r'^modify/(?P<pk>\d+)/$',permission_required('links.change_link')(LinkUpdateView.as_view()), name='link-update-view'),								
	]
