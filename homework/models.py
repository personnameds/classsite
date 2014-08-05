from django.db import models
from django.contrib.auth.models import User
from kalendar.models import Kalendar
from classlists.models import Klass

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

class Homework(models.Model):
    subject = models.CharField(max_length=10,choices=SUBJECT_CHOICES,blank=False,default='Math')
    assigned_work = models.CharField(max_length=50)
    entered_by = models.ForeignKey(User, related_name='entered_by')
    entered_on=models.DateField()


    def __unicode__(self):
        return '%s: %s' %(self.subject, self.assigned_work)

    def get_absolute_url(self):
    	return "/homework/modify/%s" %(self.id)

    class Meta:
		verbose_name='Homework'
		verbose_name_plural='Homework'

class Hwk_Details(models.Model):
    hwk=models.ForeignKey(Homework)
    due_date=models.ForeignKey(Kalendar)
    modified_by=models.ForeignKey(User, related_name='modified_by',null=True, blank=True)
    modified_on=models.DateField(blank=True, null=True)
    deleted=models.BooleanField(default=False)
    klass=models.ForeignKey(Klass, blank=True, verbose_name='Class')
    
    def __unicode__(self):
        return '%s: %s - %s' %(self.hwk.subject, self.hwk.assigned_work, self.klass)
    
   	