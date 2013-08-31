from django.conf.urls import patterns, url

from initialize.views import InitInfoTemplateView, InitTeachersFormView, InitKlassFormView, InitKalendarFormView
                             
from django.contrib.auth.decorators import user_passes_test

urlpatterns=patterns('',

    url(r'^kalendar/$', user_passes_test(lambda u: u.is_staff)(InitKalendarFormView.as_view()), name='init_kalendar'), #needs security
    url(r'^$', user_passes_test(lambda u: u.is_staff)(InitInfoTemplateView.as_view()), name='init_info'), 
    url(r'^teachers/$', user_passes_test(lambda u: u.is_staff)(InitTeachersFormView.as_view()), name='init_teachers'), 
    url(r'^klass/$', user_passes_test(lambda u: u.is_staff)(InitKlassFormView.as_view()), name='init_klass'),      
    )