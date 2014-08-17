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