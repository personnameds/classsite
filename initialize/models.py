from django.db import models
from django.forms import ModelForm

class Schedule_Format(models.Model):
    number_of_days=models.IntegerField()
    periods_per_day=models.IntegerField()
    lunch_check=models.BooleanField()
    before_check=models.BooleanField()
    after_check=models.BooleanField()
    
    class Meta:
        verbose_name="Schedule Format"

    def __unicode__(self):
		return "Schedule Format"        
    

class Schedule_Format_Form(ModelForm):
    class Meta:
        model=Schedule_Format
