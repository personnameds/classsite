from django.db import models
from django.forms import ModelForm, BooleanField

class Schedule_Setup(models.Model):
    name=models.CharField(max_length=15, verbose_name='Schedule Name')
    periods_in_day=models.PositiveSmallIntegerField(verbose_name='Periods in a Day',help_text="Count before, after, lunch and recess as periods",)
    
    def __str__(self):
        return str(self.name)
        
    class Meta:
        verbose_name='Schedule Setup'
        verbose_name_plural='Schedule Setup'

class Period_Details(models.Model):
    number=models.PositiveSmallIntegerField(verbose_name='Period #',help_text='Periods include lunch, recess, before and after school',)
    name=models.CharField(max_length=14,verbose_name='Period Name',blank=True)
    start_time=models.CharField(max_length=5, blank=True)
    end_time=models.CharField(max_length=5, blank=True)
    setup=models.ForeignKey('Schedule_Setup', blank=False)
    
    def __str__(self):
        return '%s %s' % (str(self.number),self.name)
        
    class Meta:
        verbose_name='Period Details'
        verbose_name_plural='Period Details'
        ordering=['number']

class Period_Activity(models.Model):
	activity=models.CharField(max_length=12, verbose_name='Activity')
	klass=models.ForeignKey('classlists.Klass', verbose_name='Class', blank=True)
	org=models.BooleanField(default=True,verbose_name='Original', blank=True)
	org_date=models.DateField(blank=True)
	details=models.ForeignKey('Period_Details', blank=True)
	day_no=models.ForeignKey('kalendar.Day_No', blank=True)
	
	def __str__(self):
		return '%s %s %s %s' % (self.activity, self.details, self.day_no, self.klass)

	class Meta:
		verbose_name='Period Activity'
		verbose_name_plural='Period Activities'

class Period_ActivityForm(ModelForm):
    permanent=BooleanField(label='Permanent Change',required=False)
    
    class Meta:
        model=Period_Activity
        fields=['activity',]

class Schedule_SetupForm(ModelForm):    
    class Meta:
        model=Schedule_Setup
        fields =['name','periods_in_day',]
 
class Day_ActivityForm(ModelForm):
    class Meta:
        model=Period_Activity
        fields=['activity',]

    def __init__(self, *args, **kwargs):
        super(Day_ActivityForm, self).__init__(*args, **kwargs)
        self.fields['activity'].label=False
