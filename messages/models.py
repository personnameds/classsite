from django.db import models
from django.forms import ModelForm, TextInput, Textarea, ModelChoiceField

from django.contrib.auth.models import User

from homework.models import Homework
from classlists.models import Classes
from datetime import date

class Topic(models.Model):
	topic = models.CharField(max_length=50)
	homework=models.ForeignKey(Homework, blank=True, null=True)
	last_msg=models.DateTimeField()
	class_db=models.ForeignKey(Classes)
	
 	def __unicode__(self):
 		return '%s' %(self.topic)

	def get_absolute_url(self):
		return "/messages/%s/messages" %(self.id)

class Add_Topic_Form(ModelForm):
	homework=ModelChoiceField(required=False,label='Applies to:',queryset=Homework.objects.exclude(due_date__date__lt=(date.today()))) 
	class Meta:
		model=Topic
		widgets={
			'description':TextInput(attrs={'size':'45'}),
			}
		exclude=('last_msg','class_db')


class Msg(models.Model):
	topic = models.ForeignKey(Topic)
	entered_on = models.DateTimeField()
	author = models.ForeignKey(User)
	msg_text=models.TextField()
	msg_replied_to=models.ForeignKey('self',blank=True, null=True)
	class_db=models.ForeignKey(Classes)
	

	def __unicode__(self):
		return '%s %s' %(self.author, self.msg_text)

class Add_Message_Form(ModelForm):
	class Meta:
		model=Msg
		widgets={
			'msg_text':Textarea(),
			}
		exclude=('topic','entered_on','msg_replied_to','author','class_db')




