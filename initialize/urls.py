from django.conf.urls import patterns, url

from initialize.views import InitInfoTemplateView, InitKalendarFormView, InitKlassFormView, InitStaffFormView
                             
from django.contrib.auth.decorators import user_passes_test

urlpatterns=patterns('',

    url(r'^kalendar/$', user_passes_test(lambda u: u.is_staff)(InitKalendarFormView.as_view()), name='init_kalendar'), 
    url(r'^$', user_passes_test(lambda u: u.is_staff)(InitInfoTemplateView.as_view()), name='init_info'), 
    url(r'^staff/$', user_passes_test(lambda u: u.is_staff)(InitStaffFormView.as_view()), name='init_staff'), 
    url(r'^klass/$', user_passes_test(lambda u: u.is_staff)(InitKlassFormView.as_view()), name='init_klass'),      
    )