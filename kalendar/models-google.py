from django.db import models
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User
from oauth2client.django_orm import FlowField, CredentialsField


class FlowModel(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    flow=FlowField()
    
class CredentialsModel(models.Model):
    id=models.OneToOneField(User, primary_key=True)
    credential = CredentialsField()
    
class Kalendar(models.Model):
	date=models.DateField()
	day_no=models.ForeignKey('Day_No')
	
	def __str__(self):
		return self.date.strftime("%a %b %d")
	
	class Meta:
		verbose_name='Date'
		verbose_name_plural='Calendar'
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
        widgets={'first_day_class': SelectDateWidget}
