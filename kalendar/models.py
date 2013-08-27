from django.db import models
from django.forms import ModelForm
from classlists.models import Klass
from day_no.models import Day_No
from django import forms

DAY_NOS=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('H','H'),
    )

class Kalendar(models.Model):
    date=models.DateField()
    day_no=models.CharField(max_length=1,choices=DAY_NOS,blank=False)
    day_version=models.ManyToManyField(Day_No,blank=False)
	
    class Meta:
        verbose_name='Date'
        verbose_name_plural='Calendar'

    def __unicode__(self):
	    return u'%s %s' % (self.date, self.day_no)
	


class Update_Day_No_Kalendar_Form(ModelForm):
	class Meta:
		model=Kalendar
		exclude=('day_version',)

class Event(models.Model):
    description= models.CharField(max_length=25)
    event_date=models.ForeignKey(Kalendar,blank=True,null=True)
    klass=models.ManyToManyField(Klass, blank=True, null=True)
    kksa=models.BooleanField(blank=True)
    
    def __unicode__(self):
        return self.description
    
class Add_Event_Form(ModelForm):
    kksa=forms.BooleanField(label='KKSA',required=False)
    klass=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
                                        queryset=Klass.objects.all(),
                                        required=False,
                                        label='Classes')
    class Meta:
 		model=Event
 		fields=('description','kksa','klass')


