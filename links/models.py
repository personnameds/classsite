from django.db import models
from django.forms import ModelForm, TextInput, ModelChoiceField,CheckboxSelectMultiple

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
    
class Link(models.Model):
	link=models.URLField()
	description=models.CharField(max_length=30)
	homework=models.ForeignKey(Homework, blank=True, null=True)
	klass=models.ManyToManyField(Klass, blank=True, null=True)
	subject=models.CharField(max_length=10,choices=SUBJECT_CHOICES, blank=True, null=True)

	def __unicode__(self):
		return '%s %s' %(self.description, self.link)

class Add_Link_Form(ModelForm):
	class Meta:
		model=Link
		widgets={
			'description':TextInput(attrs={'size':'30'}),
			#'class_db':CheckboxSelectMultiple(),
			}
		exclude=('class_db')

