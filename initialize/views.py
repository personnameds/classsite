from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, FormView
# from initialize.models import Schedule_Format, Schedule_Format_Form
from initialize.forms import Create_Kalendar_Form
from classlists.models import Klass, Teacher
from day_no.models import Day_No
from kalendar.models import Kalendar
from django.contrib.auth.models import User, Group, Permission
from datetime import date, timedelta

def InitKlassesCreateView(request):
    Klass.objects.all().delete()
    Teacher.objects.all().delete()
    Group.objects.all().delete()
    
    new_klass=Klass(
        klass_name='8B',
        )
    new_klass.save()
    
    new_teacher=Teacher(
        user=User.objects.get(username='sudeep'),
        klass=new_klass,
        teacher_name='Mr. Sanyal',
        )
    new_teacher.save()
    
    new_klass=Klass(
        klass_name='8A',
        )
    new_klass.save()
    
    new_teacher=Teacher(
        user=User.objects.get(username='locampo'),
        klass=new_klass,
        teacher_name='Mrs. Ocampo',
        )
    new_teacher.save()
    
    teacher_group=Group(name='Teacher Group')
    teacher_group.save()
    is_teacher=Permission.objects.get(name='Is a teacher')
    teacher_group.permissions.add(is_teacher)
    
    for t in Teacher.objects.all():
        t.user.groups.add(teacher_group,)
        
    
    return HttpResponseRedirect(reverse('init_day_create',))
    

# class InitScheduleFormatCreateView(CreateView):
# # Not needed so not used for now
# #     template_name='initialize/init_schedule_format_form.html'
# #     form_class=Schedule_Format_Form
# #     success_url='initialize/initdayformat' 
    
def InitDayCreateView(request):
    Day_No.objects.all().delete()
    
    day_list=('1P','2P','3P','4P','5P','HP','1M','2M','3M','4M','5M','HM')
    klass_list=Klass.objects.all()

    for k in klass_list:
        for i in day_list:
            new_day_no=Day_No(
                day_no=i,
                before_event="",
                period1_event="P1",			
                period2_event="P2",				
                period3_event="P3",				
                lunch_event="Lunch",
                period4_event="P4",				
                period5_event="P5",			
                period6_event="P6",						
                after_event="",	
                klass=k,
                )
            new_day_no.save()
    
    return HttpResponseRedirect(reverse('init_kalendar_create',))
    
class InitKalendarFormView(FormView):
	form_class=Create_Kalendar_Form
	template_name='initialize/create_kalendar_form.html'
	
 	def form_valid(self, form, **kwargs):
		
		last_day=date(int(self.request.POST['last_day_year']),int(self.request.POST['last_day_month']),int(self.request.POST['last_day_day']))
		first_day_school=date(int(self.request.POST['first_day_school_year']),int(self.request.POST['first_day_school_month']),int(self.request.POST['first_day_school_day']))
		first_day=date(int(self.request.POST['first_day_year']),int(self.request.POST['first_day_month']),int(self.request.POST['first_day_day']))
		
		Kalendar.objects.all().delete()

		change_day=first_day
		
		while change_day < first_day_school:
			if change_day.weekday() < 5:
				k=Kalendar(date=change_day,day_no='H')
				k.save()
			change_day=change_day + timedelta(days=1)
		
		i=1
		while change_day <= last_day:
			if change_day.weekday() < 5:
				k=Kalendar(date=change_day,day_no=str(i))
				k.save()
				if i==5:
					i=1
				else:
					i=i+1
					
			change_day=change_day + timedelta(days=1)
 		
 		return HttpResponseRedirect('/')

