from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth.models import User, Group
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from registration.forms import Registration_Form
from classlists.forms import School_StaffForm
from classlists.models import Klass, Student, School_Staff
from django.core.urlresolvers import reverse
from django.conf import settings
from classsite.views import SchoolNameMixin

class RegisterStaffFormView(SchoolNameMixin, FormView):
    form_class=School_StaffForm
    template_name='registration/registration_form.html'
    named_url='registration-staff-view'
    
    def form_valid(self, form):
        firstname=form.cleaned_data["first_name"]
        lastname=form.cleaned_data['last_name']
        firstname=firstname.replace(" ","")
        lastname=lastname.replace(" ","")
        teacher_name=form.cleaned_data["teacher_name"]

        #checks for duplicate teacher names
        #if duplicate teacher names adds a number at end
        i=1
        while True:    
            if not School_Staff.objects.filter(teacher_name=teacher_name):
                break
            teacher_name=teacher_name+str(i)
            i=i+1
  
        username=teacher_name.replace(" ","").replace(".","")

        new_user=User.objects.create_user(
                                        username=username.lower(),
                                        first_name=firstname.title(),
                                        last_name=lastname.title(),
                                        email=form.cleaned_data['email'],
                                        )
        new_user.set_password(form.cleaned_data["password1"])
        new_user.save()
        
        new_staff=School_Staff(user=new_user,
                            teacher_name=teacher_name,
                            allow_contact=True,
                            )
        new_staff.save()
        staff_group=Group.objects.get(name='Staff_Group')
        new_user.groups.add(staff_group)
        
        user=authenticate(username=new_user.username, password=form.cleaned_data["password1"])
        
        if user is not None:
            login(self.request, user)
        
        return HttpResponseRedirect(reverse('welcome-view'))  


class RegistrationFormView(SchoolNameMixin, FormView):
    form_class=Registration_Form
    template_name='registration/registration_form.html'
    named_url='registration-view'
    ### INSTEAD OF WELCOME WHY NOT EMAIL WITH PASSWORD

    def form_valid(self, form):
        new_user=form.save(commit=False)
        klass=Klass.objects.get(code=form.cleaned_data["class_code"])
            
        firstname=form.cleaned_data["first_name"]
        lastname=form.cleaned_data['last_name']
        firstname=firstname.replace(" ","")
        lastname=lastname.replace(" ","")
        
        #creates a username using the first name and first letter of last name
        i=1
        while True:
            #checks to see if there are letters in the last name to use
            if i <= len(lastname): 
                username=(firstname+lastname[:i]).lower()
            else:
                #if runs out of last name letter starts to use numbers
                username=(firstname+lastname[:i]+str(i-1)).lower()
            #if username exists loops through adding next letter of last name
            if not User.objects.filter(username=username):
                break
            i=i+1

        #adds user and creates student at the same time
        new_user.username=username        
        new_user.set_password(form.cleaned_data["password1"])
        new_user.first_name=firstname.title()
        new_user.last_name=lastname.title()
        new_user.save()

        user=authenticate(username=username, password=form.cleaned_data["password1"])
        
        if user is not None:
            login(self.request, user)

        new_student=Student(user=new_user,klass=klass)
        new_student.save()
        
        return HttpResponseRedirect(reverse('welcome-view'))     

class WelcomeView(SchoolNameMixin, TemplateView):
    template_name='registration/welcome.html'

    def get_context_data(self, **kwargs):
        user=self.request.user
        context=super(WelcomeView, self).get_context_data(**kwargs)
        context['user']=user
        return context  
        
        