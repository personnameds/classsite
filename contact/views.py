from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from classlists.models import Klass
from django.contrib.auth.models import User
from classlists.models import Teacher
from django.core.mail import EmailMessage
from contact.forms import Contact_Form

class ContactFormView(FormView):
	form_class=Contact_Form
	template_name='contact/contact.html'
	
	def get_context_data(self, **kwargs):
	    klass=self.kwargs['class_url']
	    context=super(ContactFormView, self).get_context_data(**kwargs)
	    context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    context['next']=self.request.path
	    return context

	def get_initial(self, **kwargs):
	    initial=super(ContactFormView, self).get_initial()
	    if self.request.user.is_authenticated():
	        initial['email']=self.request.user.email
	    return initial


	def form_valid(self, form):
	    klass=self.kwargs['class_url']
	    
	    subject=self.request.POST['subject']
	    message=self.request.POST['message']
	    sender=self.request.POST['email']
	    teacher=Teacher.objects.get(pk=self.request.POST['teacher'])
	    recipient=[teacher.user.email,]
	    #send_mail(subject, message, sender, recipient)

	    email=EmailMessage(subject, message, 'sudeepsanyal@sudeepsanyal.webfactional.com',
	                    recipient, headers={'Reply-To':sender})
	    email.send()

	    return HttpResponseRedirect('/'+klass)
