from django import forms
from django.forms import ModelForm
from .models import Homework
from kalendar.models import Kalendar
from classlists.models import Klass
from django.forms.widgets import CheckboxSelectMultiple, TextInput
from datetime import date

class Homework_Form(ModelForm):
    due_date=forms.ModelChoiceField(
                    queryset=Kalendar.objects.exclude(date__lte=date.today()).exclude(day_no='H'),
                    empty_label=None,
                    label='Due Date:',
                    )
    klass=forms.ModelMultipleChoiceField(
                    queryset=Klass.objects.all(),
                    widget=CheckboxSelectMultiple(),
                    label='Classes:',
                    error_messages={'required':'Please choose at least one class'},
                    )
    
    class Meta:
        model=Homework
        fields=['subject','work'] 
        
        