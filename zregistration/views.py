from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from registration.forms import Registration_Form
from classlists.models import Klass, Student
from django.core.urlresolvers import reverse

class LoginUserView(FormView):
    form_class=AuthenticationForm
    template_name='registration/login.html'
    
    def get_context_data(self, **kwargs):
        context=super(LoginUserView, self).get_context_data(**kwargs)
        context['reg_status']=settings.CLASS_REGISTRATION
        #no next for context because uses next that was given
        return context
    
    def form_valid(self, form):
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        next=self.request.GET['next']
        user=authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
        
        return HttpResponseRedirect(next)

def LogoutUserView(request):
    
    logout(request)
    return HttpResponseRedirect("/")

class RegistrationFormView(FormView):
    form_class=Registration_Form
    template_name='generic/generic_form.html'
    title='Registration'

    #no klass variable because determines klass after class_code is entered
    def get_context_data(self, **kwargs):
        context=super(RegistrationFormView, self).get_context_data(**kwargs)
        context['next']='/'
        return context 

    def form_valid(self, form):
        new_user=form.save(commit=False)
        
        #klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
            
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

        new_student=Student(student=new_user,klass=Klass.objects.get(class_code=form.cleaned_data["class_code"]))
        new_student.save()
        return HttpResponseRedirect(reverse('welcome-view'))

class WelcomeView(TemplateView):
    template_name='registration/welcome.html'

    def get_context_data(self, **kwargs):
        user=self.request.user
        context=super(WelcomeView, self).get_context_data(**kwargs)
        context['user']=user
        context['klass']=user.student.klass
        return context  