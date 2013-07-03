# from django.db import models
# from classlists.models import Classes
# from django.contrib.auth.models import User
# from django.forms import ModelForm, ValidationError
# 
# 
# ##check online I might have messed this up
# class Homepage(models.Model):
#     message=models.TextField()
#     date=models.DateField(blank=True, null=True)
#     class_db=models.ForeignKey(Classes, blank=True, null=True)
#     entered_by=models.ForeignKey(User, blank=True, null=True)
#     
#     class Meta:
#         ordering=["-date"]
# 
#     def __unicode__(self):
#         return self.message
# 
# class Homepage_Form(ModelForm):
#     class Meta:
#         model=Homepage
#         
#     def __init__(self, request, *args, **kwargs):
#         self.request=request
#         super(Homepage_Form, self).__init__(*args, **kwargs)
# 
#     def clean_entered_by(self):
#         entered_by=self.cleaned_data['entered_by']
#         if self.cleaned_data['entered_by']:
#             if not self.request.user==self.cleaned_data['entered_by']:
#                 raise ValidationError("You did not write this message.")
#         return entered_by