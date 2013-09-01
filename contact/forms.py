from django import forms
from django.contrib.auth.models import User
from classlists.models import Teacher

class Contact_Form(forms.Form):
	subject=forms.CharField(max_length=30,error_messages={'required':'Please enter a subject for this e-mail.'})
	email=forms.EmailField(error_messages={'required':'No e-mail, how will I respond?'})
	message=forms.CharField(widget=forms.Textarea,error_messages={'required':'Your message is blank?'})
	teacher=forms.ModelChoiceField(queryset=Teacher.objects.all(), empty_label=None)

	def clean_message(self):
		message = self.cleaned_data['message']
		num_words = len(message.split())
		if num_words < 4:
			raise forms.ValidationError("Not enough words!")
		return message
