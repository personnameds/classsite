from django.conf.urls.defaults import patterns, include, url
from registration.views import LoginUserView, LogoutUserView, RegistrationFormView, WelcomeView, PasswordChangeFormView, ChangedView, NotChangedView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^login/$',(LoginUserView.as_view())),
    url(r'^logout/$',(LogoutUserView.as_view())),
    url(r'^newuser/$',(RegistrationFormView.as_view())),	
  	url(r'^newuser/welcome/$',(WelcomeView.as_view())),	  	
  	url(r'^change/$',login_required(login_url='/registration/login/')(PasswordChangeFormView.as_view())),	 
  	url(r'^change/changed$',(ChangedView.as_view())), 
  	url(r'^change/notchanged$',(NotChangedView.as_view())),
	)
