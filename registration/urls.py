from django.conf.urls import url
from registration.views import RegistrationFormView, WelcomeView, RegisterStaffFormView

urlpatterns = [
    url(r'^newuser/$',RegistrationFormView.as_view(), name='registration-view'),
    url(r'^newstaff/$',RegisterStaffFormView.as_view(), name='registration-staff-view'),   	
  	url(r'^welcome/$',WelcomeView.as_view(), name='welcome-view'),	
 	]