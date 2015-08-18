from django.conf.urls import patterns, include, url
from registration.views import LoginUserView, RegistrationFormView, WelcomeView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^login/$',(LoginUserView.as_view())),
    url(r'^logout/$','registration.views.LogoutUserView'),
    url(r'^newuser/$',(RegistrationFormView.as_view())),	
  	url(r'^newuser/welcome/$',WelcomeView.as_view(), name='welcome-view'),	  	
	)
