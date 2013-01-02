from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Classes(models.Model):
    classes=models.CharField(max_length=2, unique=True)
    teacher=models.OneToOneField(User, unique=True)
    
    def __unicode__(self):
		return self.classes
		
class ClassesForm(ModelForm):
    class Meta:
        model=Classes
    
    
class UserProfile(models.Model):
    user=models.OneToOneField(User, unique=True)
    in_class=models.ForeignKey(Classes, blank=True, null=True)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)


