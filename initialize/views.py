from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView
# from initialize.models import Schedule_Format, Schedule_Format_Form
from initialize.forms import Create_Kalendar_Form, Teacher_Registration_Form, Create_Klass_Form
from classlists.models import Klass, Teacher
from day_no.models import Day_No
from kalendar.models import Kalendar
from django.contrib.auth.models import User, Group, Permission
from datetime import date, timedelta

class InitInfoTemplateView(TemplateView):
    template_name='initialize/init_info.html'

    def get_context_data(self, **kwargs):

        context=super(InitInfoTemplateView, self).get_context_data(**kwargs)

        context['next']=self.request.path
        context['klass_list']=Klass.objects.all()
        context['teacher_list']=Teacher.objects.all()
        
        try:
            if Kalendar.objects.all()[0]:
                context['kalendar']=True
            else:
                context['kalendar']=False
        except:
            pass
            
        return context
        
class InitTeachersFormView(FormView):
    form_class=Teacher_Registration_Form
    template_name='initialize/init_teacher.html'

    def form_valid(self, form):
                
        firstname=form.cleaned_data["first_name"]
        lastname=form.cleaned_data['last_name']
        firstname=firstname.replace(" ","")
        lastname=lastname.replace(" ","")
        teacher_name=form.cleaned_data["teacher_name"]
        user_name=teacher_name.replace(" ","").replace(".","")
        
        #creates a username using the teacher name
        i=1
        username=user_name.lower()
        #I don't think this works
        while True:
            if not User.objects.filter(username=username):
                break
            #add numbers if teacher name is taken            
            username=(user_name+str(i-1)).lower()
            i=i+1

        #adds user and creates student at the same time
        new_user=User.objects.create_user(
                                        username=username,
                                        first_name=firstname.title(),
                                        last_name=lastname.title(),
                                        email=form.cleaned_data['email'],
                                        )
        new_user.set_password(form.cleaned_data["password1"])
        new_user.save()
        
        new_teacher=Teacher(user=new_user,
                            teacher_name=teacher_name,
                            )
        new_teacher.save()

        try:
            teacher_group=Group.objects.get(name='Teacher Group')
            new_user.groups.add(teacher_group)
        except Group.DoesNotExist:
            teacher_group=Group(name='Teacher Group')
            teacher_group.save()
            is_teacher=Permission.objects.get(name='Is a teacher')
            teacher_group.permissions.add(is_teacher)
            new_user.groups.add(teacher_group)

        return HttpResponseRedirect('/initialize')

class InitKlassFormView(FormView):
    form_class=Create_Klass_Form
    template_name='initialize/init_klass.html'

    def form_valid(self, form):
        klass_name=form.cleaned_data['klass_name']
        teacher=form.cleaned_data['teacher']
        
        new_klass=Klass(klass_name=klass_name)
        new_klass.save()
        teacher.klass=new_klass
        teacher.save()
        
        #days are hardcoded in
        #if delete class, days do not delete
        day_list=('1P','2P','3P','4P','5P','HP','1M','2M','3M','4M','5M','HM')

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
                klass=new_klass,
                )
            new_day_no.save()     
        
        return HttpResponseRedirect('/initialize')
    
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
 		
 		return HttpResponseRedirect('/initialize')


    