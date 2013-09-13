from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from registration.forms import Registration_Form, PasswordChange_Form
from classlists.models import Klass

class LoginUserView(FormView):
    form_class=AuthenticationForm
    template_name='registration/login.html'
    
    def get_context_data(self, **kwargs):
        context=super(LoginUserView, self).get_context_data(**kwargs)
        
        try: 
            klass=self.kwargs['class_url']
        except:
            klass=self.request.GET['next']
            klass=klass[1:3]
        
        context['klass']=Klass.objects.get(klass_name=klass)
        context['path']='/'+klass
        return context
    
    def form_valid(self, form):
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        next=self.request.GET['next']
        user=authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
        
        return HttpResponseRedirect(next)

class LogoutUserView(TemplateView):
    template_name='registration/logout.html'

    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(LogoutUserView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['path']='/'+self.kwargs['class_url']
        logout(self.request)
        return context

class RegistrationFormView(FormView):
    form_class=Registration_Form
    template_name='registration/registration.html'

    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(RegistrationFormView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['path']='/'+self.kwargs['class_url']
            
        return context 

    def form_valid(self, form):
        new_user=form.save(commit=False)
        
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
            
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
        new_user.klass=klass
        new_user.save()
        
        #need to add group permissions
        
        
        #sends them an email Fail Silently is TRUE
        send_mail('Welcome to the Class '+klass.klass_name+' Website ',
 					new_user.first_name+' '+new_user.last_name+'\n'+'Username:'
 					+new_user.username+'\n'+'Password:'+form.cleaned_data["password1"]+'\n', 
 					'sudeepsanyal@sudeepsanyal.webfactional.com',
 					[new_user.email,'sudeepsanyal@sudeepsanyal.webfactional.com'],
 					)
        return HttpResponseRedirect('welcome')

class WelcomeView(TemplateView):
    template_name='registration/welcome.html'

    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(WelcomeView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['path']='/'+self.kwargs['class_url']
        return context  

class ChangedView(TemplateView):
    template_name='registration/changed.html'

    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(ChangedView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['path']='/'+self.kwargs['class_url']
        return context  

class NotChangedView(TemplateView):
    template_name='registration/notchanged.html'

    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(NotChangedView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['path']='/'+self.kwargs['class_url']
        return context  



class PasswordChangeFormView(FormView):
    form_class=PasswordChange_Form
    template_name='registration/passwordchange.html'

    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(PasswordChangeFormView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['path']='/'+self.kwargs['class_url']
        return context
        
     
    def form_valid(self, form):

        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])

        username=form.cleaned_data['username']            
        firstname=form.cleaned_data["first_name"]
        lastname=form.cleaned_data['last_name']
        email=form.cleaned_data['email']
        
        if (self.request.user.username == username) and (self.request.user.first_name == firstname) and (self.request.user.last_name == lastname) and (self.request.user.email == email):
            self.request.user.set_password(form.cleaned_data["password1"])
            self.request.user.save()
            send_mail('Password Change for '+klass.klass_name+' Website ',
 					'Username:'+username+'\n'+'Password:'+form.cleaned_data["password1"]+'\n', 
 					'sudeepsanyal@sudeepsanyal.webfactional.com',
 					[email,'sudeepsanyal@sudeepsanyal.webfactional.com'],
 					)  
            return HttpResponseRedirect('changed')          
        else:
            return HttpResponseRedirect('notchanged')  

   
