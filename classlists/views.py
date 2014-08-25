from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from classlists.models import Klass, Student
from classlists.forms import Staff_Edit_Form, Code_Edit_Form
from registration.forms import Registration_Form
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from classpage.views import URLMixin
#from registration.views import create_username

class Class_Details_ListView(ListView):
    template_name="classlists/details_list.html"
    context_object_name="student_list"
    
    def get_queryset(self):
        if Klass.objects.filter(teacher=self.request.user):
            klass=Klass.objects.get(teacher=self.request.user)
            student_list=Student.objects.filter(klass=klass)#.order_by('student__last_name')
            return student_list
        else:
            return None
        
    def get_context_data(self, **kwargs):
        teacher=self.request.user
        if Klass.objects.filter(teacher=teacher):
            klass=Klass.objects.get(teacher=teacher)
        else:
            klass=self.kwargs['class_url']
        context=super(Class_Details_ListView, self).get_context_data(**kwargs)
        context['klass']=klass #Klass is not only dependent on URL
        context['teacher']=teacher
        context['next']=self.request.path
        return context

class Staff_Edit_UpdateView(URLMixin, UpdateView):
	form_class=Staff_Edit_Form
	template_name="generic/generic_only_modify.html"
	title='Teacher'

	def get_object(self):
		return self.request.user

	def get_initial(self, **kwargs):
		user=self.object
		initial=super(Staff_Edit_UpdateView, self).get_initial()
		initial['teacher_name']=user.kksa_staff.teacher_name
		initial['allow_contact']=user.kksa_staff.allow_contact
		return initial
		
	def form_valid(self, form):
		user=form.save(commit=False)
		
		firstname=form.cleaned_data["first_name"]
		lastname=form.cleaned_data['last_name']
		firstname=firstname.replace(" ","")
		lastname=lastname.replace(" ","")
		teacher_name=form.cleaned_data['teacher_name']
		username=teacher_name.replace(" ","").replace(".","")
		
		user.username=username.lower()
		user.first_name=firstname.title()
		user.last_name=lastname.title()
		user.set_password=(form.cleaned_data["password1"])
		user.save()
		
		staff=user.kksa_staff
		staff.teacher_name=teacher_name
		staff.allow_contact=form.cleaned_data['allow_contact']
		staff.save()

		return HttpResponseRedirect(reverse('class-list-view', args=(self.kwargs['class_url'],),))

class Code_Edit_UpdateView(URLMixin, UpdateView):
	model=Klass
	form_class=Code_Edit_Form
	template_name="generic/generic_only_modify.html"
	title='Class Code'

	def get_object(self):
		return Klass.objects.get(teacher=self.request.user)
	
	def get_success_url(self):
	    a=self.kwargs['class_url']
	    return reverse('class-list-view', args=(self.kwargs['class_url'],),)

class Student_Edit_UpdateView(URLMixin, UpdateView):
    model=User
    form_class=Registration_Form
    template_name='generic/generic_only_modify.html'
    title='Student'
    
    def get_form(self, form_class):
        form=super(Student_Edit_UpdateView, self).get_form(form_class)
        form.fields.pop('class_code')
        return form
    
    def form_valid(self, form):
	    user=form.save(commit=False)
	    firstname=form.cleaned_data["first_name"]
	    lastname=form.cleaned_data['last_name']
	    firstname=firstname.replace(" ","")
	    lastname=lastname.replace(" ","")
	    #username=create_username(firstname,lastname)
	    
	    #adds user and creates student at the same time
	    #user.username=username
	    user.set_password(form.cleaned_data["password1"])
	    user.first_name=firstname.title()
	    user.last_name=lastname.title()
	    user.save()
	    
	    return HttpResponseRedirect(reverse('class-list-view', args=(self.kwargs['class_url'],),))
