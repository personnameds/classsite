from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from classsite.views import URLMixin
from django.views.generic.list import ListView
from .models import Student, Klass
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from registration.forms import Registration_Form2

class ClasslistsView(URLMixin, ListView):
	template_name='classlists/classlist.html'
	context_object_name='classlist'

	def get_queryset(self):
	    return Student.objects.filter(klass__name=self.kwargs['class_url'])
	    
class StudentCreateView(URLMixin, CreateView):
    model=User
    template_name='generic/generic_form.html'
    title='Student'
    named_url='student-create-view'
    form_class=Registration_Form2
    
    def form_valid(self, form):
        new_user=form.save(commit=False)
        klass=Klass.objects.get(name=self.kwargs['class_url'])
            
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

        new_student=Student(user=new_user,klass=klass)
        new_student.save()
        
        return HttpResponseRedirect(reverse('classlists-view', args=(self.kwargs['class_url'],)))
    
    
    

class StudentUpdateView(URLMixin, UpdateView):
    model=User
    template_name='generic/generic_modify.html'
    title='Student'
    named_url='student-update-view'
    form_class=Registration_Form2

    def form_valid(self, form):
    
        if self.request.POST['mod/del']=='Delete':
            del_user=self.object
            if self.request.user.has_perm('homework.delete_student'):
                del_user.delete()
        else:
            mod_user=form.save(commit=False)
            
            firstname=form.cleaned_data["first_name"]
            lastname=form.cleaned_data['last_name']
            firstname=firstname.replace(" ","")
            lastname=lastname.replace(" ","")
            
            mod_user.first_name=firstname.title()
            mod_user.last_name=lastname.title()
            mod_user.set_password(form.cleaned_data["password1"])
            mod_user.save()
            
        return HttpResponseRedirect(reverse('classlists-view', args=(self.kwargs['class_url'],)))
   