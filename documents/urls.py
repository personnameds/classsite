from django.conf.urls import url
from .views import DocumentListView, DocumentCreateView, DocumentUpdateView
from django.contrib.auth.decorators import permission_required

urlpatterns = [
	url(r'^$', DocumentListView.as_view(), name='document-list-view'),
	url(r'^add/$',permission_required('documents.add_document')(DocumentCreateView.as_view()), name='document-create-view'),
	url(r'^modify/(?P<pk>\d+)/$',permission_required('documents.change_document')(DocumentUpdateView.as_view()), name='document-update-view'),
	]
