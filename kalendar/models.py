from django.db import models
from django.forms import ModelForm,TextInput, DateField, CheckboxSelectMultiple
from classlists.models import Classes
from day_no.models import Day_No
from django.forms import ModelChoiceField

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
	
	def __unicode__(self):
 		return u'%s %s' % (self.date, self.day_no)

class Update_Day_No_Kalendar_Form(ModelForm):
	class Meta:
		model=Kalendar
		exclude=('day_version',)

class Event(models.Model):
	description= models.CharField(max_length=25)
	event_date=models.ForeignKey(Kalendar,blank=True,null=True)
	class_db=models.ManyToManyField(Classes, blank=True, null=True)
			
 	def __unicode__(self):
 		return self.description

class EventModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.date
        
class Add_Event_Form(ModelForm):
	event_date=EventModelChoiceField(queryset=Kalendar.objects.all(), empty_label=None, required=False)
	class Meta:
		model=Event
		widgets={
			'description':TextInput(attrs={'size':'25'}),
			'class_db':CheckboxSelectMultiple(),
			}