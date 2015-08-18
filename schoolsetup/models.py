from django.db import models


class Schedule_Setup(models.Model):
	days_in_cycle=models.PositiveSmallIntegerField(verbose_name='Days in a Cycle')
	periods_in_day=models.PositiveSmallIntegerField(verbose_name='Periods in a Day')
	lunch_start=models.CharField(max_length=5, verbose_name='Lunch Start')
	lunch_end=models.CharField(max_length=5, verbose_name='Lunch End')
	before_start=models.CharField(max_length=5, verbose_name='Before Start')
	before_end=models.CharField(max_length=5, verbose_name='Before End')
	after_start=models.CharField(max_length=5, verbose_name='After Start')
	after_end=models.CharField(max_length=5, verbose_name='After End')
	
	class Meta:
		verbose_name='Schedule Setup'
		verbose_name_plural='Schedule Setup'

class Period_Details(models.Model):
	number=models.PositiveSmallIntegerField(verbose_name='Perod #')
	start_time=models.CharField(max_length=5)
	end_time=models.CharField(max_length=5)
	schedule=models.ForeignKey('Schedule_Setup')
	
	def __str__(self):
		return str(self.number)
	
	class Meta:
		verbose_name='Period Details'
		verbose_name_plural='Period Details'

class Recess_Details(models.Model):
	number=models.PositiveSmallIntegerField(verbose_name='Recess #')
	start_time=models.CharField(max_length=5)
	end_time=models.CharField(max_length=5)
	schedule=models.ForeignKey('Schedule_Setup')
	
	class Meta:
		verbose_name='Recess Details'
		verbose_name_plural='Recess Details'



