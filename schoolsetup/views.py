from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from schedule.models import Schedule_Setup, Schedule_SetupForm
from schedule.models import Period_Details
from kalendar.models import Kalendar_Setup, Kalendar_SetupForm, Kalendar, Day_No
from classlists.models import Klass, StaffCode, School_Staff
from classlists.forms import School_StaffForm
from django.contrib.auth.models import User, Group
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from datetime import date, timedelta


##SETUP HOMEPAGE
class SchoolSetupView(TemplateView):
    template_name='schoolsetup/setup_info.html'

    def get_context_data(self, **kwargs):
        context=super(SchoolSetupView, self).get_context_data(**kwargs)
        context['school_name']=settings.SCHOOL
        context['kalendar']=Kalendar.objects.all().exists()
        if Schedule_Setup.objects.all().exists():
            context['schedule_setups']=Schedule_Setup.objects.all()
        context['klass_count']=Klass.objects.all().count() 
        context['staff_count']=School_Staff.objects.all().count()
        context['staffcode']=StaffCode.objects.all().exists
        return context


## KALENDAR SETUP
class KalendarSetupView(TemplateView):
    template_name='schoolsetup/kalendar_info.html'
    
    def get_context_data(self, **kwargs):
        context=super(KalendarSetupView, self).get_context_data(**kwargs)
        context['school_name']=settings.SCHOOL
        if Kalendar_Setup.objects.all().exists():
            context['kalendar_setup']=Kalendar_Setup.objects.get(name=settings.SCHOOL)
            context['day_no_list']=Day_No.objects.all()
        return context

class KalendarSetupCreateView(CreateView):
    model=Kalendar_Setup
    template_name='schoolsetup/add_kalendar_setup.html'
    form_class=Kalendar_SetupForm
    
    def get_initial(self):
        return {'first_day_class': date(date.today().year,9,1)}
    
    def form_valid(self, form):
        Kalendar_Setup.objects.all().delete()
        Day_No.objects.all().delete()
        
        kalendar_setup=form.save(commit=False)
        kalendar_setup.name=settings.SCHOOL
        kalendar_setup.save()
        
        DayNoCreate(kalendar_setup.days_in_cycle)
        KalendarCreate(kalendar_setup.first_day_class, kalendar_setup.days_in_cycle)
        
        return HttpResponseRedirect(reverse('kalendar-setup-view',))

def KalendarCreate(first_day_class, days_in_cycle):
    Kalendar.objects.all().delete()
    day=date(first_day_class.year, 8, 1)
    last_day=date(first_day_class.year+1, 6, 30)
    
    while day < first_day_class:
        holiday=Day_No.objects.get(day_name='H')
        if day.weekday() < 5:
            k=Kalendar(date=day, day_no=holiday)
            k.save()
        day=day + timedelta(days=1)

    i=1
    while day <= last_day:
        if day.weekday()<5:
            k=Kalendar(date=day, day_no=Day_No.objects.get(day_name=str(i)))
            k.save()
            if i==days_in_cycle:
                i=1
            else:
                i=i+1
        day=day + timedelta(days=1)
    
    while day <= date(first_day_class.year+1, 7, 31):
        if day.weekday() < 5:
            k=Kalendar(date=day, day_no=Day_No.objects.get(day_name='H'))
            k.save()
        day=day + timedelta(days=1)


def DayNoCreate(days_in_cycle):
    for day in range(1,days_in_cycle+1):
        day_name=Day_No(day_name=day)
        day_name.save()
    day_name=Day_No(day_name='H')
    day_name.save()



## SCHEDULE SETUP

class ScheduleSetupView(TemplateView):
    template_name='schoolsetup/schedule_info.html'
    
    def get_context_data(self, **kwargs):
        context=super(ScheduleSetupView, self).get_context_data(**kwargs)
        context['school_name']=settings.SCHOOL
        if Schedule_Setup.objects.all().exists():
            schedule_list=[]
            for s in Schedule_Setup.objects.all():
                schedule_list.append((s, s.period_details_set.all()))
            context['schedule_list']=schedule_list
        return context

class ScheduleSetupCreateView(CreateView):
    model=Schedule_Setup
    template_name='schoolsetup/add_schedule_setup.html'
    form_class=Schedule_SetupForm

    def form_valid(self, form):
        schedule_setup=form.save()
        return HttpResponseRedirect(reverse('period-details-create-view',kwargs={'setup_id':schedule_setup.pk}))

class ScheduleSetupUpdateView(UpdateView):
    model=Schedule_Setup
    template_name='schoolsetup/modify_schedule_setup.html'
    form_class=Schedule_SetupForm
    
    def form_valid(self, form):
        schedule_setup=form.save(commit=False)
        if self.request.POST['mod/del']=='Delete':
            schedule_setup.delete()
        else:
            schedule_setup.save()

        return HttpResponseRedirect(reverse('schedule-setup-view',))


class PeriodDetailsCreateView(CreateView):
    model=Period_Details
    template_name='schoolsetup/add_period_details.html'
    
    def get_form_class(self):
        extra=Schedule_Setup.objects.get(pk=self.kwargs['setup_id']).periods_in_day
        return inlineformset_factory(Schedule_Setup, Period_Details,fields=('name','start_time','end_time',),can_delete=False,extra=extra,)

    def form_valid(self, form):
        setup=Schedule_Setup.objects.get(pk=self.kwargs['setup_id'])
        period_num=0
        for f in form:
            period_num+=1
            per_detail=f.save(commit=False)
            per_detail.number=period_num
            per_detail.setup=setup
            per_detail.save()

        return HttpResponseRedirect(reverse('schedule-setup-view',))

class KlassSetupView(TemplateView):
    template_name='schoolsetup/class_info.html'
    
    def get_context_data(self, **kwargs):
        context=super(KlassSetupView, self).get_context_data(**kwargs)
        context['school_name']=settings.SCHOOL
        if Klass.objects.all().exists():
            context['klass_list']=Klass.objects.all()
        return context

class KlassCreateView(CreateView):
    model=Klass
    template_name='schoolsetup/add_klass.html'
    fields=['name','url','code','schedule']
    success_url=reverse_lazy('class-setup-view')

class KlassUpdateView(UpdateView):
    model=Klass
    template_name='schoolsetup/change_klass.html'
    fields=['name','url','code','schedule']
    
    
    def form_valid(self, form):
        klass=form.save(commit=False)
        if self.request.POST['mod/del']=='Delete':
            klass.delete()
        else:
            klass.save()

        return HttpResponseRedirect(reverse('class-setup-view',))

##STAFF SETUP
class StaffSetupView(TemplateView):
    template_name='schoolsetup/staff_info.html'
    
    def get_context_data(self, **kwargs):
        context=super(StaffSetupView, self).get_context_data(**kwargs)
        context['school_name']=settings.SCHOOL
        if StaffCode.objects.all().exists():
            context['staffcode']=StaffCode.objects.get(school=settings.SCHOOL)
        if School_Staff.objects.all().exists():
            context['staff_list']=School_Staff.objects.all()
        return context

class StaffCodeCreateView(CreateView):
    model=StaffCode
    template_name='schoolsetup/add_staffcode.html'
    fields=['code']
    
    def form_valid(self, form):
        code=form.save(commit=False)
        code.school=settings.SCHOOL
        code.save()
        return HttpResponseRedirect(reverse('staff-setup-view',))

class StaffCodeUpdateView(UpdateView):
    model=StaffCode
    template_name='schoolsetup/change_staffcode.html'
    fields=['code',]
    
    
    def form_valid(self, form):
        code=form.save(commit=False)
        if self.request.POST['mod/del']=='Delete':
            code.delete()
        else:
            code.school=settings.SCHOOL
            code.save()

        return HttpResponseRedirect(reverse('staff-setup-view',))

class StaffCreateView(FormView):
    template_name='schoolsetup/add_staff.html'
    form_class=School_StaffForm
    
    def form_valid(self, form):

        firstname=form.cleaned_data["first_name"]
        lastname=form.cleaned_data['last_name']
        firstname=firstname.replace(" ","")
        lastname=lastname.replace(" ","")
        teacher_name=form.cleaned_data["teacher_name"]
        
        user_name=teacher_name.replace(" ","").replace(".","")

        new_user=User.objects.create_user(
                                        username=user_name.lower(),
                                        first_name=firstname.title(),
                                        last_name=lastname.title(),
                                        email=form.cleaned_data['email'],
                                        )
        new_user.set_password(form.cleaned_data["password1"])
        new_user.save()
        
        new_staff=School_Staff(user=new_user,
                            teacher_name=teacher_name,
                            allow_contact=form.cleaned_data['allow_contact'],
                            )
        new_staff.save()
        staff_group=Group.objects.get(name='Staff_Group')
        new_user.groups.add(staff_group)

        return HttpResponseRedirect(reverse('staff-setup-view',))
