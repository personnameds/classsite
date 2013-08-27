from django.conf.urls.defaults import patterns, include, url
from documents.views import DocumentListView, DocumentCreateView, DocumentUpdateView

urlpatterns = patterns('',
	url(r'^$', DocumentListView.as_view(), name='document_view'),
 	url(r'^add/$',DocumentCreateView.as_view()),
 	url(r'^modify/(?P<pk>\d+)/$',DocumentUpdateView.as_view()),
 							
	)
