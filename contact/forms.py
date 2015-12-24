from django import forms
from django.contrib.auth.models import User
from classlists.models import School_Staff

class Contact_Form(forms.Form):
	subject=forms.CharField(max_length=30,error_messages={'required':'Please enter a subject for this e-mail.'})
	name=forms.CharField(max_length=30, error_messages={'required':'No name, how will I know who this e-mail is from?'}) 
	email=forms.EmailField(label='Your E-mail', error_messages={'required':'No e-mail, how will I respond?'})
	staff=forms.ModelChoiceField(queryset=School_Staff.objects.filter(allow_contact=True))
	message=forms.CharField(widget=forms.Textarea,error_messages={'required':'Your message is blank?'})
	
	def clean_message(self):
		message = self.cleaned_data['message']
		num_words = len(message.split())
		if num_words < 4:
			raise forms.ValidationError("Not enough words!")
		return message