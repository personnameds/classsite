from django.db import models
from classlists.models import Klass
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError, ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

class Classpage(models.Model):
    message=models.TextField()
    date=models.DateField(blank=True, null=True)
    klass=models.ForeignKey(Klass, blank=True, null=True, verbose_name='Class')
    entered_by=models.ForeignKey(User, blank=True, null=True)

    def entered_by_display(self):
        return self.entered_by.kksa_staff.teacher_name
    entered_by_display.short_description='Entered By'

    class Meta:
        verbose_name='Classpage'
        verbose_name_plural='Classpage'        

class Classpage_Form(ModelForm):
    klass=ModelMultipleChoiceField(
                            queryset=Klass.objects,
                            widget=CheckboxSelectMultiple(),
                            label='Class:',
                            error_messages={'required':'Please choose at least one class'},
                            )
                            
    class Meta:
        model=Classpage
        fields =['message']
