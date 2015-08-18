from django import forms
from django.forms.extras.widgets import SelectDateWidget
from classlists.models import KKSA_Staff

from datetime import date

class Staff_Registration_Form(forms.Form):
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
    					max_length=20,
    					)

    email=forms.EmailField(
    					label='Email',
    					)

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password again", widget=forms.PasswordInput)
    
    allow_contact=forms.BooleanField(
                            label="Allow Email Contact",
                            required=False,
                            )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

class Create_Kalendar_Form(forms.Form):
	first_day_school=forms.DateField(initial=date(date.today().year,9,1),widget=SelectDateWidget()) 
	first_day=forms.DateField(initial=date(date.today().year,9,1),widget=SelectDateWidget())
	last_day=forms.DateField(initial=date(date.today().year+1,8,31),widget=SelectDateWidget())


class Create_Klass_Form(forms.Form):
    teacher=forms.ModelChoiceField(label='Teacher', queryset=KKSA_Staff.objects.all())
    klass_name=forms.CharField(label='Class Name', max_length=2)
    class_code=forms.CharField(max_length=10)
