from django.db import models
from django.contrib.auth.models import User

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

class Homework(models.Model):
    entered_by = models.ForeignKey(User)
    entered_on=models.DateField()
    subject=models.CharField(max_length=15,choices=SUBJECT_CHOICES,blank=False,default='Math')
    work=models.CharField(
            max_length=50,
            error_messages={'required':'Please enter what needs to be done'},
            verbose_name='Assigned Work:',
            )

    
    class Meta:
        verbose_name='Homework'
        verbose_name_plural='Homework'
        permissions=(("can_add_multi_classes", "Can add to multiple classes"),)

    def __str__(self):
        return '%s: %s' %(self.subject, self.work)
   
class Hwk_Details(models.Model):
    homework=models.ForeignKey(Homework)
    due_date=models.ForeignKey('kalendar.Kalendar')
    modified_by=models.ForeignKey(User, blank=True, null=True)
    modified_on=models.DateField(blank=True, null=True)
    deleted=models.BooleanField(default=False)
    klass=models.ForeignKey('classlists.Klass', verbose_name='Class')
    
    def __str__(self):
        return '%s: %s' %(self.homework.subject, self.homework.work)