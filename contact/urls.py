from django.conf.urls.defaults import patterns, include, url

from contact.views import ContactFormView

urlpatterns = patterns('',
	url(r'^$', ContactFormView.as_view()),
	)
