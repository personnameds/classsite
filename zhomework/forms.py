from django import forms
from django.forms import ModelForm
from homework.models import Hwk_Details
from kalendar.models import Kalendar
from classlists.models import Klass
from django.forms.widgets import CheckboxSelectMultiple, TextInput
#from django.forms.extras.widgets import SelectDateWidget
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

class Hwk_Details_Staff_Form(ModelForm):
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

    #Document form fields
    attached_file=forms.FileField(label='Attached file (Optional):', required=False)
    document_description=forms.CharField(
					max_length=30, 
					label='Document Description (Optional if attaching a file):',
					required=False,
					)

    #Link form fields
    link=forms.URLField(required=False,
                        widget=TextInput(attrs={'size':'200'}),
                        label='Link (Optional):',
                        )
    link_description=forms.CharField(
                    max_length=30,
    				label='Link Description (Required if adding a Link):',
    				required=False,
    				)
    				
    def clean(self):
        cleaned_data=super(Hwk_Details_Staff_Form, self).clean()
        link=cleaned_data.get('link')
        link_description=cleaned_data.get('link_description')
        
        if link:
        	if not link_description:
                    raise forms.ValidationError('The added Link needs a description.')
        return self.cleaned_data