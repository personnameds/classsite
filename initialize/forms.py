from django import forms
from django.forms.extras.widgets import SelectDateWidget

from datetime import date

class Create_Kalendar_Form(forms.Form):
	first_day_school=forms.DateField(initial=date(date.today().year,9,1),widget=SelectDateWidget()) 
	first_day=forms.DateField(initial=date(date.today().year,9,1),widget=SelectDateWidget())
	last_day=forms.DateField(initial=date(date.today().year+1,8,31),widget=SelectDateWidget())
