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

class Add_Day_No_Form(forms.ModelForm):
    change_type=forms.ChoiceField(choices=(('P','Permanent'),('M','For This Week')), label='Change will be:', initial='M')

    class Meta:
        model=Day_No
        fields=('change_type','before_event','period1_event','period2_event','period3_event','lunch_event','period4_event','period5_event','period6_event','after_event')

    def __init__(self, request, class_url, *args, **kwargs):
        self.request=request
        self.class_url=class_url
        super(Add_Day_No_Form, self).__init__(*args, **kwargs)

#     def clean(self):
#         if self.request.user.get_profile().in_class.classes != self.class_url:
#             raise forms.ValidationError("This is not your class.")
#         return self.cleaned_data
        
        