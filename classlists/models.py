from django.db import models
from django.contrib.auth.models import User

class Klass(models.Model):
	name=models.CharField(max_length=12, verbose_name='Class', unique=True)
	url=models.CharField(max_length=4, verbose_name='Class Url', unique=True)
	code=models.CharField(max_length=10, verbose_name='Class Code')
	#teacher
	#banner
	
	class Meta:
		verbose_name='Class'
		verbose_name_plural='Classes'
	
	def __str__(self):
		return self.name
		
class Student(models.Model):
    user=models.OneToOneField(User, verbose_name='User Name')
    klass=models.ForeignKey('Klass', verbose_name='Class')
    
    def full_name(self):
        return '%s %s ' %(self.user.first_name, self.user.last_name)
    full_name.short_description='Name'
    
    def __str__(self):
    	return self.user.username
		
class School_Staff(models.Model):
    user=models.OneToOneField(User)
    teacher_name=models.CharField(max_length=20, unique=True)
    allow_contact=models.BooleanField(default=False)
    
    class Meta:
        verbose_name='Staff'
        verbose_name_plural='Staff'
        
    def __str__(self):
    	return self.teacher_name


