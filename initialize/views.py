from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from initialize.forms import Create_Kalendar_Form, Create_Klass_Form, Staff_Registration_Form
from classlists.models import Klass, KKSA_Staff
from day_no.models import Day_No
from kalendar.models import Kalendar
from django.contrib.auth.models import User, Group, Permission
from datetime import date, timedelta
from django.conf import settings

class InitInfoTemplateView(TemplateView):
    template_name='initialize/init_info.html'

    def get_context_data(self, **kwargs):

        context=super(InitInfoTemplateView, self).get_context_data(**kwargs)

        context['next']='/'
        klass_list=[]
        for k in Klass.objects.all():
            klass_list.append((k,k.teacher))
        context['klass_list']=klass_list
        context['staff_list']=KKSA_Staff.objects.all()
        
        try:
            if Kalendar.objects.all()[0]:
                context['kalendar']=True
            else:
                context['kalendar']=False
        except:
            pass
        
        context['reg_status']=settings.CLASS_REGISTRATION
        
        return context
        
class InitStaffFormView(FormView):
    form_class=Staff_Registration_Form
    template_name='initialize/init_teacher.html'

    def form_valid(self, form):
                
        firstname=form.cleaned_data["first_name"]
        lastname=form.cleaned_data['last_name']
        firstname=firstname.replace(" ","")
        lastname=lastname.replace(" ","")
        teacher_name=form.cleaned_data["teacher_name"]
        user_name=teacher_name.replace(" ","").replace(".","")

        #adds user and creates staff at the same time
        new_user=User.objects.create_user(
                                        username=user_name.lower(),
                                        first_name=firstname.title(),
                                        last_name=lastname.title(),
                                        email=form.cleaned_data['email'],
                                        )
        new_user.set_password(form.cleaned_data["password1"])
        new_user.save()
        
        new_staff=KKSA_Staff(user=new_user,
                            teacher_name=teacher_name,
                            allow_contact=form.cleaned_data['allow_contact'],
                            )
        new_staff.save()

        try:
            staff_group=Group.objects.get(name='KKSA Staff')
            new_user.groups.add(staff_group)
        except Group.DoesNotExist:
            staff_group=Group(name='KKSA Staff')
            staff_group.save()
            is_kksastaff=Permission.objects.get(name='Is on KKSA Staff')
            staff_group.permissions.add(is_kksastaff)
            new_user.groups.add(staff_group)

        return HttpResponseRedirect('/initialize')

class InitKlassFormView(FormView):
    form_class=Create_Klass_Form
    template_name='generic/generic_form.html'

    def form_valid(self, form):
        klass_name=form.cleaned_data['klass_name']
        teacher=form.cleaned_data['teacher']     
        class_code=form.cleaned_data['class_code']  
        new_klass=Klass(klass_name=klass_name, teacher=teacher, class_code=class_code)
        new_klass.save()
        
        #days are hardcoded in
        #if delete class, days do not delete
        day_list=('1P','2P','3P','4P','5P','HP','1M','2M','3M','4M','5M','HM')

        for i in day_list:
            new_day_no=Day_No(
                day_name=i,
                before="",
                p1="P1",			
                p2="P2",				
                p3="P3",				
                lunch="Lunch",
                p4="P4",				
                p5="P5",			
                p6="P6",						
                after="",	
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
