from django.conf.urls import url

from contact.views import ContactFormView

urlpatterns = [
	url(r'^$', ContactFormView.as_view(),name='contact-view'),
	]
