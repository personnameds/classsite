from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError


class Schoolpage(models.Model):
    message=models.TextField()
    date=models.DateField(blank=True, null=True)
    entered_by=models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return u'%s : %s' % (self.message, self.entered_by)

class Schoolpage_Form(ModelForm):
    class Meta:
        model=Schoolpage
        
    def __init__(self, request, *args, **kwargs):
        self.request=request
        super(Schoolpage_Form, self).__init__(*args, **kwargs)

    def clean_entered_by(self):
        entered_by=self.cleaned_data['entered_by']
        if self.cleaned_data['entered_by']:
            if not self.request.user==self.cleaned_data['entered_by']:
                raise ValidationError("You did not write this message.")
        return entered_by