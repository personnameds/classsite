from django.conf.urls.defaults import patterns, include, url
from documents.views import DocumentListView, DocumentCreateView, DocumentUpdateView
from django.contrib.auth.decorators import user_passes_test

urlpatterns = patterns('',
	url(r'^$', DocumentListView.as_view(), name='document-list-view'),
 	url(r'^add/$',user_passes_test(lambda u:u.is_staff)(DocumentCreateView.as_view())),
 	url(r'^modify/(?P<pk>\d+)/$',user_passes_test(lambda u:u.is_staff)(DocumentUpdateView.as_view())),
 							
	)
