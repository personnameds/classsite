from django.conf.urls.defaults import patterns, include, url
from registration.views import LoginUserView, LogoutUserView, RegistrationFormView, WelcomeView

urlpatterns = patterns('',
    url(r'^login/$',(LoginUserView.as_view())),
    url(r'^logout/$',(LogoutUserView.as_view())),
    url(r'^newuser/$',(RegistrationFormView.as_view())),	
 	url(r'^newuser/welcome/$',(WelcomeView.as_view())),	
	)


