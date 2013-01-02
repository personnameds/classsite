from django.db import models
from django.forms import ModelForm, TextInput, ModelChoiceField,CheckboxSelectMultiple

from homework.models import Homework
from classlists.models import Classes

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

class Document(models.Model):
	attached_file=models.FileField(upload_to='attachments') ##for whatever reason upload_to='documents' not recognized
	filename=models.CharField(max_length=300)	
	description=models.CharField(max_length=30, blank=True)
	homework=models.ForeignKey(Homework, blank=True, null=True)
	class_db=models.ManyToManyField(Classes, blank=True, null=True)
	subject=models.CharField(max_length=10,choices=SUBJECT_CHOICES, blank=True, null=True)

	def __unicode__(self):
		return self.filename
		
class Add_Document_Form(ModelForm):
	class Meta:
		model=Document
		widgets={
			'description':TextInput(attrs={'size':'30'}),
			#'class_db':CheckboxSelectMultiple(),
			}
		exclude=('filename','class_db')
