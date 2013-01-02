from django import forms
from django.contrib.auth.models import User

class Registration_Form(forms.ModelForm):
    first_name = forms.CharField(
    					label='First Name',
    					max_length=15,
    					error_messages={'required':'You need to enter your first name.'},
						 )
    last_name = forms.CharField(
    		    		label='Last Name',
    					max_length=15,
    					error_messages={'required':'You need to enter your last name.'},
    					)
    email=forms.EmailField(
    					label='Email',
    					help_text='Should look something like email@example.com',
    					error_messages={'required':'No e-mail, how will I respond?'},
    					)

    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password again"), widget=forms.PasswordInput,
        help_text = ("Same password as above, for verification."))
	
    class Meta:
        model = User
        fields=('first_name','last_name','email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2
