from django.db import models
from django import forms
from classlists.models import Klass

class Day_No(models.Model):
    day_no=models.CharField(max_length=2, blank=True)
    before_event=models.CharField(blank=True,max_length=10)
    period1_event=models.CharField(max_length=10)
    period2_event=models.CharField(max_length=10)
    period3_event=models.CharField(max_length=10)
    lunch_event=models.CharField(max_length=10)
    period4_event=models.CharField(max_length=10)
    period5_event=models.CharField(max_length=10)
    period6_event=models.CharField(max_length=10)
    after_event=models.CharField(max_length=10, blank=True)
    klass=models.ForeignKey(Klass, null=True)

    class Meta:
        verbose_name="Day Number"
