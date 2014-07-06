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
    day_no=models.CharField(max_length=1,choices=DAY_NOS)
    
    def __unicode__(self):
        return '%s Day %s' %(self.date.strftime("%a %b %d"), self.day_no)

#     def __unicode__(self):
#         return '%s: %s' %(self.subject, self.assigned_work)
        	
    class Meta:
        verbose_name='Date'
        verbose_name_plural='Calendar'

class Update_Day_No_Kalendar_Form(ModelForm):
	class Meta:
		model=Kalendar

class Event(models.Model):
    description= models.CharField(max_length=25)
    event_date=models.ForeignKey(Kalendar,blank=True,null=True)
    klass=models.ManyToManyField(Klass, blank=True, null=True)
    kksa=models.BooleanField(blank=True)
    
    def __unicode__(self):
        return self.description
    
    def klass_names(self):
        return ', '.join([k.klass_name for k in self.klass.all()])
    klass_names.short_description="Classes"
    
class Add_Event_Form(ModelForm):
    kksa=forms.BooleanField(label='KKSA',required=False)
    klass=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
                                        queryset=Klass.objects.all(),
                                        required=False,
                                        label='Classes')
    class Meta:
 		model=Event
 		fields=('description','kksa','klass')


