from django import forms
from classlists.models import StaffCode, School_Staff
from django.contrib.auth.models import User

class School_StaffForm(forms.Form):
    first_name = forms.CharField(
    					label='First Name',
    					max_length=25,
    					error_messages={'required':'You need to enter your first name.'},
						 )
    last_name = forms.CharField(
    		    		label='Last Name',
    					max_length=25,
    					error_messages={'required':'You need to enter your last name.'},
    					)
    teacher_name = forms.CharField(
    		    		label='Teacher Name',
    					max_length=25,
    					help_text="How the student's refer to you.",
    					error_messages={'required':'You need to enter your teacher name.'},
    					)
    email=forms.EmailField(
    					label='Email',
    					required=False,
    					help_text='Should look something like email@example.com',
    					)
    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password again"), widget=forms.PasswordInput,
        help_text = ("Same password as above, for verification."))
    
    staff_code=forms.CharField(
                        label="Staff Code",
                        help_text='Your website admininstrator it',
                        error_messages={"required":"You can't register without it."},
                        widget=forms.PasswordInput
	                    )
	            
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def clean_staff_code(self):
        staff_code=self.cleaned_data.get("staff_code","")
        if not StaffCode.objects.filter(code=staff_code):
            raise forms.ValidationError("The staff code is not correct")
        return staff_code
