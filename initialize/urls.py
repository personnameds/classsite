from django.conf.urls import patterns, url

from initialize.views import InitKlassesCreateView, InitDayCreateView, InitKalendarFormView
        #InitScheduleFormatCreateView, InitDayFormatCreateView

urlpatterns=patterns('',
    url(r'^$', InitKlassesCreateView), #needs security
#   Right now whole initial creation is skipped because hard coded    
#    url(r'^initscheduleformat/$', InitScheduleFormatCreateView.as_view(), name='init_schedule_format'), #needs security
#   in future this will be a createview to make day creation based on schedule format   
#   for now it is hardcoded
    url(r'^initdaycreate/$', InitDayCreateView, name='init_day_create'), #needs security 
    
    url(r'^initkalendar/$', InitKalendarFormView.as_view(), name='init_kalendar_create'), #needs security
    
    )