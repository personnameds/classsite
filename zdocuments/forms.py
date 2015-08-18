from django import forms
from django.forms import ModelForm
from documents.models import Document
from classlists.models import Klass
from django.forms.widgets import CheckboxSelectMultiple, TextInput
from homework.models import Hwk_Details
from datetime import date, timedelta

class Add_Document_Form(ModelForm):

    hwk_details=forms.ModelChoiceField(
            queryset=Hwk_Details.objects.exclude(due_date__date__lt=(date.today())),
            label='Related Homework:',
            required=False,
            )    
    klass=forms.ModelMultipleChoiceField(
            queryset=Klass.objects.all(),
            widget=CheckboxSelectMultiple(),
            label='Classes:',
            required=True,
            error_messages={'required':'Please choose at least one class'},
            )
    
    
    def clean(self):
        cleaned_data=super(Add_Document_Form, self).clean()
        detail=cleaned_data.get('hwk_details')
        klass=cleaned_data.get('klass')
        
        if detail:
            homework=detail.hwk
            for k in klass:
                if not homework.hwk_details_set.filter(klass=k):
                    raise forms.ValidationError(k.klass_name+' does not have that for homework.')
        return self.cleaned_data
        
    class Meta:
        model=Document
        widgets={
            'description':TextInput(attrs={'size':'30'}),
            }
        fields=['attached_file','description','subject','klass']
        
        
