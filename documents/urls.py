from django.conf.urls import patterns, url
from .views import DocumentListView, DocumentCreateView, DocumentUpdateView
from django.contrib.auth.decorators import permission_required

urlpatterns = patterns('',
	url(r'^$', DocumentListView.as_view(), name='document-list-view'),
	url(r'^add/$',permission_required('document.add_document')(DocumentCreateView.as_view()), name='document-create-view'),
	url(r'^modify/(?P<pk>\d+)/$',permission_required('document.change_document')(DocumentUpdateView.as_view()), name='document-update-view'),
	)
