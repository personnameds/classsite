from django.db import models
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
	klass=models.ManyToManyField(Klass, blank=False)
	subject=models.CharField(max_length=10,choices=SUBJECT_CHOICES, blank=True, null=True)
	
	def __unicode__(self):
		return '%s %s' %(self.description, self.link)

