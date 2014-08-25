from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from classlists.models import Klass
from django.contrib.auth.models import User
from classlists.models import KKSA_Staff
from django.core.mail import EmailMessage
from contact.forms import Contact_Form
from django.core.urlresolvers import reverse
from classpage.views import URLMixin

class ContactFormView(URLMixin, FormView):
	form_class=Contact_Form
	template_name='contact/contact.html'
	title='Contact'

	def get_initial(self, **kwargs):
	    initial=super(ContactFormView, self).get_initial()
	    if self.request.user.is_authenticated():
	        initial['email']=self.request.user.email
	        initial['name']=self.request.user.first_name + ' ' + self.request.user.last_name
	    return initial

	def form_valid(self, form):
	    sender_name=form.cleaned_data['name']+' sent from KKSA.ca'
	    subject=form.cleaned_data['subject']
	    message=form.cleaned_data['message']
	    sender_email=form.cleaned_data['email']
	    staff=form.cleaned_data['staff']
	    recipient=[staff.user.email,]

	    email=EmailMessage(subject, message, sender_name,
	                    recipient, headers={'Reply-To':sender_email})
	    email.send()

	    return HttpResponseRedirect(reverse('homepage-list-view', args=(self.kwargs['class_url'],),))
