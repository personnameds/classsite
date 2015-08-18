from django import forms
from classlists.models import Klass
from django.contrib.auth.models import User

class Staff_Edit_Form(forms.ModelForm):
    first_name = forms.CharField(
    					label='First Name',
    					max_length=15,
						 )
    last_name = forms.CharField(
    		    		label='Last Name',
    					max_length=15,
    					)

    teacher_name = forms.CharField(
    		    		label='Teacher Name',
    					max_length=15,
    					)

    email=forms.EmailField(
    					label='Email',
    					)

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password again", widget=forms.PasswordInput)
    
    allow_contact=forms.BooleanField(
                            label="Allow Email Contact",
                            required=True,
                            )
    
    class Meta:
    	model=User
    	fields=['first_name','last_name','email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

class Code_Edit_Form(forms.ModelForm):
	class Meta:
		model=Klass
		fields=['class_code']