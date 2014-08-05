from django.db import models
from django.forms import ModelForm, TextInput, ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from homework.models import Homework
from classlists.models import Klass

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
    ('Misc','Misc.'),
    )

def upload_to(instance, filename):
     return 'documents/%s/%s' % (instance.subject, filename)

class Document(models.Model):
	attached_file=models.FileField(upload_to=upload_to)
	filename=models.CharField(max_length=300)	
	description=models.CharField(max_length=30, blank=True)
	homework=models.ForeignKey(Homework, blank=True, null=True)
	klass=models.ManyToManyField(Klass, blank=True, verbose_name='Class')
	subject=models.CharField(
	                        max_length=10,
	                        choices=SUBJECT_CHOICES,
	                        default='Misc',
	                        )	
	
	def klass_list(self):
	    return ', '.join([k.klass_name for k in self.klass.all()])
	klass_list.short_description='Classes'
	
class Add_Document_Form(ModelForm):
	class Meta:
		model=Document
		widgets={
			'description':TextInput(attrs={'size':'30'}),
			}
		fields=['attached_file','description','homework','subject','klass']

        klass=ModelMultipleChoiceField(
                            queryset=Klass.objects,
                            widget=CheckboxSelectMultiple(),
                            label='Class:',
                            error_messages={'required':'Please choose at least one class'},
                            )