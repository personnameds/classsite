from django import forms
from django.forms import ModelForm
from homework.models import Hwk_Details
from kalendar.models import Kalendar
from classlists.models import Klass
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from datetime import date, timedelta


class Hwk_Details_Form(ModelForm):
    class Meta:
        model=Hwk_Details
        fields=['subject','assigned_work','due_date']


    assigned_work = forms.CharField(
                        max_length=50, 
                        widget=forms.TextInput(attrs={'size':'45'}),
                        error_messages={'required':'Please enter what needs to be done'},
                        label='Assigned Work:',
                        )    
                        
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

