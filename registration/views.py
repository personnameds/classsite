from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from registration.forms import Registration_Form
from classlists.models import Classes, UserProfile
from django.contrib.auth.models import User, Group

class LoginUserView(FormView):
    form_class=AuthenticationForm
    template_name='registration/login.html'
    
    def get_context_data(self, **kwargs):
	    class_url=self.kwargs['class_url']
	    context=super(LoginUserView, self).get_context_data(**kwargs)
	    context['class_url']=class_url.lower()
	    return context
	
    def form_valid(self, form):
        username=form.cleaned_data["username"]
        password=form.cleaned_data["password"]
        class_url=self.kwargs['class_url']
        
        user=authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect('/'+class_url)

class LogoutUserView(TemplateView):
    template_name='registration/logout.html'

    def get_context_data(self, **kwargs):
	    class_url=self.kwargs['class_url']
	    context=super(LogoutUserView, self).get_context_data(**kwargs)
	    context['class_url']=class_url.lower()
	    logout(self.request)
	    return context  

class RegistrationFormView(FormView):
    model=User
    form_class=Registration_Form
    template_name='registration/registration.html'
    
    def form_valid(self, form):
        new_user=form.save(commit=False)
        
        class_db=Classes.objects.get(classes=self.kwargs['class_url'])

        firstname=form.cleaned_data["first_name"]
        lastname=form.cleaned_data['last_name']
        firstname=firstname.replace(" ","")
        lastname=lastname.replace(" ","")
        
        i=1
        while True:

            username=(firstname+lastname[:i]).lower()
            #username=(form.cleaned_data["first_name"]+form.cleaned_data['last_name'][:i]).lower()
            i=i+1
            if not User.objects.filter(username=username):
                break

        new_user.username=username        
        new_user.set_password(form.cleaned_data["password1"])
        new_user.first_name=firstname.title()
        new_user.last_name=lastname.title()
        #new_user.first_name=form.cleaned_data["first_name"].title()
        #new_user.last_name=form.cleaned_data["last_name"].title()
        new_user.save()
        
        new_user.get_profile().in_class=class_db
        new_user.get_profile().save()
        
        send_mail('Class 8B Website',
 					new_user.first_name+' '+new_user.last_name+'\n'+'Username:'+new_user.username+'\n'+'Password:'+form.cleaned_data["password1"]+'\n'+class_db.classes, 
 					'sudeepsanyal@sudeepsanyal.webfactional.com',
 					[new_user.email,'sudeepsanyal@sudeepsanyal.webfactional.com'],
 					)
        return HttpResponseRedirect('welcome')
        
    def get_context_data(self, **kwargs):
	    class_url=self.kwargs['class_url']
	    context=super(RegistrationFormView, self).get_context_data(**kwargs)
	    context['class_url']=class_url.lower()
	    logout(self.request)
	    return context  

class WelcomeView(TemplateView):
    template_name='registration/welcome.html'

    def get_context_data(self, **kwargs):
	    class_url=self.kwargs['class_url']
	    context=super(WelcomeView, self).get_context_data(**kwargs)
	    context['class_url']=class_url.lower()
	    logout(self.request)
	    return context  

def unknownlogin(request):
    class_url=request.GET['next'][1:3]
    return HttpResponseRedirect('/'+class_url+'/registration/login/')