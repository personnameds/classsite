from django.db import models
from django.contrib.auth.models import User
from homework.models import Homework
from classlists.models import Klass
from datetime import date

class Topic(models.Model):
	topic = models.CharField(max_length=50)
	homework=models.ForeignKey(Homework, blank=True, null=True)
	last_msg=models.DateTimeField()
	klass=models.ForeignKey(Klass)
	
 	def __unicode__(self):
 		return '%s' %(self.topic)

	def get_absolute_url(self):
		return "/messages/%s/messages" %(self.id)

class Msg(models.Model):
	topic = models.ForeignKey(Topic)
	entered_on = models.DateTimeField()
	author = models.ForeignKey(User)
	msg_text=models.TextField()
	msg_replied_to=models.ForeignKey('self',blank=True, null=True)
	klass=models.ForeignKey(Klass)
	
	def __unicode__(self):
		return '%s %s' %(self.author, self.msg_text)