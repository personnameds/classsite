from django.db import models
from django.contrib.auth.models import User
from classlists.models import School_Staff, Klass
from django.forms import ModelForm, ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

class Classpage(models.Model):
    message=models.TextField()
    date=models.DateField()
    klass=models.ManyToManyField('classlists.Klass', verbose_name='Class')
    entered_by=models.ForeignKey(User)

    def klass_display(self):
    	return ", ".join([k.name for k in self.klass.all()])
    klass_display.short_description='Classes'

    def entered_by_display(self):
        if School_Staff.objects.filter(user=self.entered_by).exists():
            return self.entered_by.school_staff.teacher_name
        else:
            return self.entered_by.first_name
    entered_by_display.short_description='Entered By'

    class Meta:
        verbose_name='Class Message'
        verbose_name_plural='Class Messages'
        ordering=['-date']

class Classpage_AddForm(ModelForm):
    klass=ModelMultipleChoiceField(
                            queryset=Klass.objects,
                            widget=CheckboxSelectMultiple(),
                            label='Class:',
                            error_messages={'required':'Please choose at least one class'},
                            )

    class Meta:
        model=Classpage
        fields =['message']

class Classpage_ModifyForm(ModelForm):
    klass=ModelMultipleChoiceField(
                            queryset=Klass.objects,
                            widget=CheckboxSelectMultiple(),
                            label='Classes:',
                            error_messages={'required':'Please choose at least one class'},
                            )
    class Meta:
        model=Classpage
        fields =['message']
