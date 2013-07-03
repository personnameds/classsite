from django.db import models
# from django.forms import ModelForm
from django.contrib.auth.models import User
# from django.db.models.signals import post_save

class Klass(models.Model):
    klass_name=models.CharField(max_length=2, unique=True)
    banner=models.ImageField(upload_to='banners')
    #teacher=models.OneToOneField(User, unique=True)
    
    class Meta:
        verbose_name="Class"
        verbose_name_plural="Classes"
    
    def __unicode__(self):
		return self.klass_name

class Student(models.Model):
    # for more info on how to use and access related information
    # for more info on how to display inline in admin
    # lower down says can use django.db.models.signals.post_save to update model when created
    # https://docs.djangoproject.com/en/1.5/topics/auth/customizing/#extending-user

    user=models.OneToOneField(User)
    klass=models.ForeignKey('Klass') 

    def __unicode__(self):
        return u'%s %s in %s' % (self.user.first_name, self.user.last_name, self.klass)





# class ClassesForm(ModelForm):
#     class Meta:
#         model=Classes
#     
#     
# class UserProfile(models.Model):
#     user=models.OneToOneField(User, unique=True)
#     in_class=models.ForeignKey(Classes, blank=True, null=True)
#     
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         profile, created = UserProfile.objects.get_or_create(user=instance)
# 
# post_save.connect(create_user_profile, sender=User)
# 
# 
