from django import forms
from django.contrib.auth.models import User

class TeacherModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name

class Contact_Form(forms.Form):
	subject=forms.CharField(max_length=30,error_messages={'required':'Please enter a subject for this e-mail.'})
	email=forms.EmailField(error_messages={'required':'No e-mail, how will I respond?'})
	message=forms.CharField(widget=forms.Textarea,error_messages={'required':'Your message is blank?'})
	teacher=TeacherModelChoiceField(queryset=User.objects.filter(is_staff=True), empty_label=None)

	def clean_message(self):
		message = self.cleaned_data['message']
		num_words = len(message.split())
		if num_words < 4:
			raise forms.ValidationError("Not enough words!")
		return message
