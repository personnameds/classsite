from django.conf.urls import patterns, url

from contact.views import ContactFormView

urlpatterns = patterns('',
	url(r'^$', ContactFormView.as_view()),
	)
