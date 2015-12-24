from django.db import models
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.models import User
from homework.models import Homework, Hwk_Details
from classlists.models import Klass
from datetime import date

class Topic(models.Model):
	topic = models.CharField(max_length=50)
	homework=models.ForeignKey(Homework, blank=True, null=True)
	last_msg=models.DateTimeField()
	klass=models.ForeignKey(Klass)
	
	def __str__(self):
		return self.topic

class Msg(models.Model):
	topic = models.ForeignKey(Topic)
	entered_on = models.DateTimeField()
	author = models.ForeignKey(User)
	msg_text=models.TextField()
	msg_replied_to=models.ForeignKey('self',blank=True, null=True)
	klass=models.ForeignKey(Klass)
	
	def __str__(self):
		return '%s %s' %(self.author, self.msg_text)
		
class Add_TopicForm(ModelForm):

    hwk_details=ModelChoiceField(
            queryset=Hwk_Details.objects.all(),
            label='Related Homework:',
            required=False,
            )    
        
    class Meta:
        model=Topic
        fields=['topic',]
		

class Add_MessageForm(ModelForm):
	class Meta:
		model=Msg
		fields=['msg_text',]
