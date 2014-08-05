from django.conf.urls import patterns, include, url
from documents.views import DocumentListView, DocumentCreateView, DocumentUpdateView
from django.contrib.auth.decorators import permission_required

urlpatterns = patterns('',
	url(r'^$', DocumentListView.as_view(), name='document_view'),
 	url(r'^add/$',permission_required('classlists.is_teacher', login_url='/registration/login/')(DocumentCreateView.as_view())),
 	url(r'^modify/(?P<pk>\d+)/$',permission_required('classlists.is_teacher', login_url='/registration/login/')(DocumentUpdateView.as_view())),
 							
	)
