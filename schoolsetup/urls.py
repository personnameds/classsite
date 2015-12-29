from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from .views import SchoolSetupView, KalendarSetupView, KalendarSetupCreateView
from .views import ScheduleSetupView, ScheduleSetupCreateView, ScheduleSetupUpdateView, PeriodDetailsCreateView
from .views import KlassSetupView, KlassCreateView, KlassUpdateView
from .views import StaffSetupView, StaffCodeCreateView, StaffCodeUpdateView, StaffCreateView


urlpatterns = [
     url(r'^$', permission_required('schedule.add_schedule_setup')(SchoolSetupView.as_view()), name='school-setup-view'),
     url(r'(?i)kalendar/$', permission_required('kalendar.add_kalendar')(KalendarSetupView.as_view()), name='kalendar-setup-view'),   
     url(r'(?i)kalendar/addcalendar$', permission_required('kalendar.add_kalendar')(KalendarSetupCreateView.as_view()), name='kalendar-setup-create-view'),   
     url(r'^(?i)schedule/$', permission_required('schedule.add_schedule_setup')(ScheduleSetupView.as_view()), name='schedule-setup-view'),
     url(r'^(?i)schedule/addschedulesetup/$', permission_required('schedule.add_schedule_setup')(ScheduleSetupCreateView.as_view()), name='schedule-setup-create-view'),
     url(r'^(?i)schedule/modifyschedulesetup/(?P<pk>\d+)/$', permission_required('schedule.change_school_setup')(ScheduleSetupUpdateView.as_view()), name='schedule-setup-update-view'),
     url(r'^(?i)schedule/perioddetails/(?P<setup_id>\d+)/$', permission_required('schedule.add_period_details')(PeriodDetailsCreateView.as_view()), name='period-details-create-view'),
     url(r'^(?i)classes/$', permission_required('classlists.add_klass')(KlassSetupView.as_view()), name='class-setup-view'),
     url(r'^(?i)classes/addclass/$', permission_required('classlists.add_klass')(KlassCreateView.as_view()), name='class-create-view'),
     url(r'^(?i)classes/changeclass/(?P<pk>\d+)/$', permission_required('classlists.change_klass')(KlassUpdateView.as_view()), name='class-update-view'),
     url(r'^(?i)staff/$', permission_required('classlists.add_school_staff')(StaffSetupView.as_view()), name='staff-setup-view'),
     url(r'^(?i)staff/addcode/$', permission_required('classlists.add_staffcode')(StaffCodeCreateView.as_view()), name='staffcode-create-view'),
     url(r'^(?i)staff/changecode/(?P<pk>\w+)/$', permission_required('classlists.change_staffcode')(StaffCodeUpdateView.as_view()), name='staffcode-update-view'),
     url(r'^(?i)staff/addstaff/$', permission_required('classlists.add_school_staff')(StaffCreateView.as_view()), name='staff-create-view'),
     ]