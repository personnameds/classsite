from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from classlists.models import Classes
from django.contrib.auth.models import User
from django.core.mail import send_mail
from contact.forms import Contact_Form

class ContactFormView(FormView):
	form_class=Contact_Form
	template_name='contact/contact.html'
	
	def get_context_data(self, **kwargs):
	    class_url=self.kwargs['class_url']
	    context=super(ContactFormView, self).get_context_data(**kwargs)
	    context['class_url']=class_url.lower()
	    return context

	def get_initial(self, **kwargs):
	    initial=super(ContactFormView, self).get_initial()
	    if self.request.user.is_authenticated():
	        initial['email']=self.request.user.email
	    return initial


	def form_valid(self, form):
	    class_url=self.kwargs['class_url']
	    
	    class_db=Classes.objects.get(classes=self.kwargs['class_url'])
	    
	    subject=self.request.POST['subject']
	    message=self.request.POST['message']
	    sender=self.request.POST['email']
	    teacher=Classes.objects.get(pk=self.request.POST['teacher']).teacher
	    recipient=[teacher.email]

	    send_mail(subject, message, sender, recipient)
	    
	    return HttpResponseRedirect('/'+class_url+'/')
