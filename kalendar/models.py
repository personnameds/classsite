from django.db import models
from classlists.models import Klass
from django.forms import ModelForm, ModelChoiceField, CheckboxSelectMultiple, ModelMultipleChoiceField
from django.forms.extras.widgets import SelectDateWidget

class Kalendar(models.Model):
	date=models.DateField(blank=True)
	day_no=models.ForeignKey('Day_No')
	
	def __str__(self):
		return self.date.strftime("%a %b %d")
	
	class Meta:
		verbose_name='Date'
		verbose_name_plural='Dates'
		ordering=['date',]
		
class Day_No(models.Model):
	day_name=models.CharField(primary_key=True, max_length=2)
	
	def __str__(self):
		return self.day_name
	
	class Meta:
	    ordering=['day_name',]
	    verbose_name='Day #'
	    verbose_name_plural="Day #'s"
	    
class Kalendar_Setup(models.Model):
    name=models.CharField(primary_key=True, max_length=15, verbose_name='Calendar Setup Name')
    first_day_class=models.DateField()
    days_in_cycle=models.PositiveSmallIntegerField(verbose_name='Days in Cycle',)
    
    def __str__(self):
        return str(self.name)
        
    class Meta:
        verbose_name='Calendar Setup'
        verbose_name_plural='Calendar Setup'
        
class Kalendar_SetupForm(ModelForm):
    class Meta:
        model=Kalendar_Setup
        fields=['first_day_class','days_in_cycle']
        widgets={'first_day_class': SelectDateWidget(years=range(2015,2020))}

class Change_Day_NoForm(ModelForm):
    date_from=ModelChoiceField(label='Date from:', empty_label=None, queryset=Kalendar.objects.all())
    date_until=ModelChoiceField(label='Date until:', queryset=Kalendar.objects.all())
    day_no=ModelChoiceField(empty_label=None, label='New Day Number:', queryset=Day_No.objects.all())
    
    class Meta:
        model=Kalendar
        fields=['date_from','date_until','day_no']
        
class Event(models.Model):
    description= models.CharField(max_length=25)
    event_date=models.ForeignKey(Kalendar,blank=True,null=True)
    klass=models.ManyToManyField(Klass, blank=True)
    
    def __unicode__(self):
        return self.description
    
    def klass_names(self):
        return ', '.join([k.name for k in self.klass.all()])
    klass_names.short_description="Classes"
    
class Event_Form(ModelForm):
    klass=ModelMultipleChoiceField(widget=CheckboxSelectMultiple, 
                                        queryset=Klass.objects.all(),
                                        required=False,
                                        label='Classes')
    class Meta:
        model=Event
        fields=('description','klass')