from django.db import models
from classlists.models import Klass
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError


class Homepage(models.Model):
    message=models.TextField()
    date=models.DateField(blank=True, null=True)
    klass=models.ForeignKey(Klass, blank=True, null=True, verbose_name='Class')
    entered_by=models.ForeignKey(User, blank=True, null=True)

    def entered_by_display(self):
        return self.entered_by.kksa_staff.teacher_name
    entered_by_display.short_description='Entered By'

    class Meta:
        verbose_name='Class Homepage Message'
        verbose_name_plural='Class Homepage Messages'        

class Homepage_Form(ModelForm):
    class Meta:
        model=Homepage
        
    def __init__(self, request, *args, **kwargs):
        self.request=request
        super(Homepage_Form, self).__init__(*args, **kwargs)

    def clean_entered_by(self):
        entered_by=self.cleaned_data['entered_by']
        if self.cleaned_data['entered_by']:
            if not self.request.user==self.cleaned_data['entered_by']:
                raise ValidationError("You did not write this message.")
        return entered_by