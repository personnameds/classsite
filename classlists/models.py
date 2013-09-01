from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Klass(models.Model):
    klass_name=models.CharField(max_length=2, unique=True)
    banner=models.ImageField(upload_to='banners',blank=True)
    
    class Meta:
        verbose_name="Class"
        verbose_name_plural="Classes"
    
    def __unicode__(self):
		return self.klass_name

# class Student(models.Model):
#     # for more info on how to use and access related information
#     # for more info on how to display inline in admin
#     # https://docs.djangoproject.com/en/1.5/topics/auth/customizing/#extending-user
# 
#     user=models.OneToOneField(User)
#     klass=models.ForeignKey('Klass', verbose_name='Class') 
# 
#     def __unicode__(self):
#         return u'%s %s in %s' % (self.user.first_name, self.user.last_name, self.klass)

# @receiver(post_save, sender=User)
# def create_student(sender, instance, created, **kwargs):
#     if created:
#         Student.objects.create(user=instance, klass=instance.klass)

class Teacher(models.Model):
    user=models.OneToOneField(User)
    klass=models.ForeignKey('Klass', verbose_name='Class',blank=True,null=True)
    teacher_name=models.CharField(max_length=20)

    class Meta:
        permissions=(('is_teacher', 'Is a teacher'),)
        
    def __unicode__(self):
        return self.teacher_name
        
