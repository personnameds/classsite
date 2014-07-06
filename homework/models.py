from django.db import models
from django import forms
from django.contrib.auth.models import User
from kalendar.models import Kalendar
from classlists.models import Klass
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from datetime import date, timedelta

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
    due_date=models.ForeignKey(Kalendar)
    entered_by = models.ForeignKey(User, related_name='entered_by')
    entered_on=models.DateField()
    modified_by=models.ForeignKey(User, related_name='modified_by',null=True, blank=True)
    modified_on=models.DateField(blank=True, null=True)
    deleted=models.BooleanField(default=False)
    klass=models.ManyToManyField(Klass, blank=True, null=True)

    def klass_names(self):
        return ', '.join([k.klass_name for k in self.klass.all()])
    klass_names.short_description="Classes"

#     def __unicode__(self):
#         return '%s: %s' %(self.subject, self.assigned_work)

    def get_absolute_url(self):
    	return "/homework/modify/%s" %(self.id)

    class Meta:
		ordering=['due_date__date']
		verbose_name='Homework'
		verbose_name_plural='Homework'
		

class Homework_Form(ModelForm):
    class Meta:
        model=Homework
        fields=['subject','assigned_work','due_date','klass']

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
                            queryset=Klass.objects,
                            widget=CheckboxSelectMultiple(),
                            label='Class:',
                            error_messages={'required':'Please choose at least one class'},
                            )

    def clean_due_date(self):
        due_date=self.cleaned_data['due_date']
        if due_date.day_no=='H':
            raise forms.ValidationError("This can't be due on a holiday")
        return due_date

