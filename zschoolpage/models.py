from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError


class Schoolpage(models.Model):
    message=models.TextField()
    date=models.DateField(blank=True, null=True)
    entered_by=models.ForeignKey(User, blank=True, null=True)

    class Meta:
        verbose_name='School Message'
        verbose_name_plural='School Messages'

    def entered_by_display(self):
        return self.entered_by.kksa_staff.teacher_name
    entered_by_display.short_description='Entered By'


class Schoolpage_Form(ModelForm):
    class Meta:
        model=Schoolpage      


##Do I need this???
    def __init__(self, request, *args, **kwargs):
        self.request=request
        super(Schoolpage_Form, self).__init__(*args, **kwargs)


    def clean_entered_by(self):
        entered_by=self.cleaned_data['entered_by']
        if self.cleaned_data['entered_by']:
            if not self.request.user==self.cleaned_data['entered_by']:
                raise ValidationError("You did not write this message.")
        return entered_by