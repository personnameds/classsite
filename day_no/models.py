from django.db import models

class Day_No(models.Model):
	day_name=models.CharField(max_length=2)
	klass=models.ForeignKey('classlists.Klass', verbose_name='Class')
	
	def __str__(self):
		return self.day_name
		
	class Meta:
		verbose_name='Day #'

class Period(models.Model):
	day_no=models.ForeignKey('Day_No', verbose_name='Day #')
	activity=models.CharField(max_length=12)
	details=models.ForeignKey('schoolsetup.Period_Details', verbose_name='Period #')
	modified=models.BooleanField(default=False, verbose_name='Modified')

	def __str__(self):
		return '%s %s' % (self.day_no.day_name, self.day_no.klass.klass_name)