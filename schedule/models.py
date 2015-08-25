from django.db import models

class Day_No(models.Model):
	day_name=models.CharField(max_length=2)
	
	def __str__(self):
		return self.day_name
	
	class Meta:
		verbose_name='Day #'
		verbose_name_plural="Day #'s"

class Period_Details(models.Model):
	number=models.PositiveSmallIntegerField(
		unique=True, 
		verbose_name='Period #',
		help_text='Periods include lunch, recess, before and after school',
		)
	name=models.CharField(max_length=14,verbose_name='Period Name')
	start_time=models.CharField(max_length=5)
	end_time=models.CharField(max_length=5)
	
	def __str__(self):
		return '%s %s' % (str(self.number),self.name)
	
	class Meta:
		verbose_name='Period Details'
		verbose_name_plural='Period Details'
		ordering=['number']

class Period_Activity(models.Model):
	activity=models.CharField(max_length=12, verbose_name='Activity')
	klass=models.ForeignKey('classlists.Klass', verbose_name='Class')
	org=models.BooleanField(default=True,verbose_name='Original')
	details=models.ForeignKey('Period_Details')
	day_no=models.ForeignKey('Day_No')
	
	def __str__(self):
		return '%s %s %s %s' % (self.activity, self.details, self.day_no, self.klass)

	class Meta:
		verbose_name='Period Activity'
		verbose_name_plural='Period Activities'



