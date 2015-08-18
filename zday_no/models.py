from django.db import models
from django import forms
from django.forms import widgets
from classlists.models import Klass
from django.utils.translation import ugettext_lazy as _

class Day_No(models.Model):
    day_name=models.CharField(max_length=2)
    klass=models.ForeignKey(Klass)

    before=models.CharField(max_length=12, blank=True)
    p1=models.CharField(max_length=12)
    p2=models.CharField(max_length=12)
    p3=models.CharField(max_length=12)
    lunch=models.CharField(max_length=12, blank=True)
    p4=models.CharField(max_length=12)
    p5=models.CharField(max_length=12)
    p6=models.CharField(max_length=12)
    after=models.CharField(max_length=12, blank=True)
    
    def __unicode__(self):
        return self.day_name

    class Meta:
        verbose_name="Day Number"

class Update_Day_No_Form(forms.ModelForm):
    change_type=forms.ChoiceField(choices=(('P','Permanent'),('M','For This Week')), label='Change will be:', initial='M')
    
    class Meta:
        model=Day_No
        fields=('change_type','before','p1','p2','p3','lunch','p4','p5','p6','after')
        labels = {
            'before': _('Before School'),
            'p1': _('Period 1'),
            'p2': _('Period 2'),
            'p3': _('Period 3'),
            'lunch': _('Lunch'),
            'p4': _('Period 4'),
            'p5': _('Period 5'),
            'p6': _('Period 6'),
            'after': _('After School'),
            }
