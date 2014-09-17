from django.db import models
from django.contrib.auth.models import User

class KKSA_Staff(models.Model):
    user=models.OneToOneField(User)
    teacher_name=models.CharField(max_length=20, unique=True)
    allow_contact=models.BooleanField(default=False)
    
    class Meta:
        permissions=(
                    ('is_kksastaff', 'Is on KKSA Staff'),
                    ('can_edit_class','Can Edit Class Lists'),
                    )
        verbose_name='Staff'
        verbose_name_plural='Staff'
        
    def __unicode__(self):
        return self.teacher_name

class Klass(models.Model):
    klass_name=models.CharField(max_length=2, verbose_name='Class', unique=True)
    banner=models.ImageField(upload_to='banners',blank=True)
    teacher=models.OneToOneField('KKSA_Staff', blank=True)
    class_code=models.CharField(max_length=10, verbose_name='Class Code', unique=True)
    
    class Meta:
        verbose_name="Class"
        verbose_name_plural="Classes"
    
    def __unicode__(self):
		return self.klass_name

    def banner_tag(self):
        return u'<img src="%s" />' %('/media/banners/'+'banner_sizing_1.jpg')
    banner_tag.short_description = 'Banner'
    banner_tag.allow_tags = True


class Student(models.Model):
    student=models.OneToOneField(User, verbose_name='User Name')
    klass=models.ForeignKey('Klass', verbose_name='Class')
    
    def full_name(self):
        return '%s %s ' %(self.student.first_name, self.student.last_name)
    full_name.short_description='Name'
