from django.db import models

class Kalendar(models.Model):
	date=models.DateField()
	day_no=models.ForeignKey('schedule.Day_No')
	
	def __str__(self):
		return self.date.strftime("%a %b %d")
	
	class Meta:
		verbose_name='Date'
		verbose_name_plural='Calendar'
		