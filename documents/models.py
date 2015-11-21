from django.db import models
from homework.models import Hwk_Details
from classlists.models import Klass
from kalendar.models import Kalendar
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField, ValidationError
from django.forms.widgets import CheckboxSelectMultiple, TextInput
from datetime import date

SUBJECT_CHOICES = (
    ('Language','Language'),
    ('Math','Math'),
    ('Science','Science'),
    ('French','French'),
    ('Visual Art','Visual Art'),
    ('Phys Ed.','Phys Ed.'),
    ('Geography','Geography'),
    ('History','History'),
    ('Drama','Drama'),
    ('Dance','Dance'),
    ('Media','Media'),    
    ('Music','Music'),    
    ('Health','Health'),
    ('Library','Library'),
    ('Misc.','Misc.'),
    )

def upload_to(instance, filename):
     return 'documents/%s/%s' % (instance.subject, filename)

class Document(models.Model):
	attached_file=models.FileField(upload_to=upload_to)
	filename=models.CharField(max_length=300)
	description=models.CharField(max_length=30, blank=True)
	homework=models.ForeignKey('homework.Homework', blank=True, null=True)
	klass=models.ManyToManyField('classlists.Klass', verbose_name='Class')
	subject=models.CharField(
	                        max_length=10,
	                        choices=SUBJECT_CHOICES,
	                        default='Misc.',
	                        )
	def __str__(self):
	    return '%s: %s' %(self.subject, self.filename)

	                        
class Add_DocumentForm(ModelForm):
    hwk_details=ModelChoiceField(
            queryset=Hwk_Details.objects.all(),
            label='Related Homework:',
            required=False,
            )
    
    klass=ModelMultipleChoiceField(
            queryset=Klass.objects.all(),
            widget=CheckboxSelectMultiple(),
            label='Classes:',
            required=True,
            error_messages={'required':'Please choose at least one class'},
            )
    
    def clean(self):
        cleaned_data=super(Add_DocumentForm, self).clean()
        detail=cleaned_data.get('hwk_details')
        klass=cleaned_data.get('klass')
        
        if not klass:
            raise ValidationError('Choose at least one class')
        
        if detail:
            homework=detail.homework
            for k in klass:
                if not homework.hwk_details_set.filter(klass=k):
                    raise ValidationError(k.name+' does not have that for homework.')
        return self.cleaned_data
        
    class Meta:
        model=Document
        widgets={
            'description':TextInput(attrs={'size':'30'}),
            }
        fields=['attached_file','description','subject','klass']

