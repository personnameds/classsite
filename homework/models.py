from django.db import models
from django import forms
from django.contrib.auth.models import User
from kalendar.models import Kalendar
from classlists.models import Klass
from django.forms import ModelForm, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from datetime import date, timedelta

SUBJECT_CHOICES = (
    ('Language','Language'),
    ('Math','Math'),
    ('Science','Science'),
    ('French','French'),
    ('Visual Art','Visual Art'),
    ('Phys Ed.','Phys Ed.'),
    ('Geography','Geography'),
    ('History','History'),
    ('Drama','Drama'),
    ('Dance','Dance'),
    ('Media','Media'),    
    ('Music','Music'),    
    ('Health','Health'),
    ('Library','Library'),
    ('Misc','Misc.'),
    )

class Homework(models.Model):
    subject = models.CharField(max_length=10,choices=SUBJECT_CHOICES,blank=False,default='Math')
    assigned_work = models.CharField(max_length=50)
    due_date=models.ForeignKey(Kalendar)
    entered_by = models.ForeignKey(User, related_name='entered_by') ##until user is added
    entered_on=models.DateField()
    modified_by=models.ForeignKey(User, related_name='modified_by',null=True, blank=True) ##until user is added
    modified_on=models.DateField(blank=True, null=True)
    deleted=models.BooleanField(default=False)
    klass=models.ManyToManyField(Klass, blank=True, null=True)
    
    class Meta:
		ordering=['due_date__date']
			
    def __unicode__(self):
        return '%s: %s' %(self.subject, self.assigned_work)


    def get_absolute_url(self):
    	return "/homework/modify/%s" %(self.id)

class Homework_Form(ModelForm):
    class Meta:
        model=Homework
        exclude=('entered_by','entered_on','modified_by','modified_on','deleted','klass')
#         widgets={
#             'class_db':CheckboxSelectMultiple(),
#             }
    assigned_work = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'size':'45'}),error_messages={'required':'Please enter what needs to be done'})
    
    if (date.today().weekday() == 4) or (date.today().weekday() == 5):
        duedate=date.today()+timedelta(days=(7-date.today().weekday()))
    else:
        duedate=date.today()+timedelta(days=1)
    due_date=forms.DateField(initial=duedate,widget=SelectDateWidget())


    def __init__(self, request, klass, *args, **kwargs):
        self.request=request
        self.klass=klass
        super(Homework_Form, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.request.user.is_staff:
            if self.request.user.get_profile().in_class.classes != self.class_url:
                raise forms.ValidationError("This is not your class.")
        return self.cleaned_data

    def clean_due_date(self):
        due_date=self.cleaned_data['due_date']
        if due_date == date.today():
            raise forms.ValidationError("Can't be due today!")
        elif (due_date.weekday()==5) or (due_date.weekday()==6):
            raise forms.ValidationError("Can't be due on the weekend!")
        elif due_date < date.today():
            raise forms.ValidationError("Can't go back in time to hand it in")
        
        due_date=Kalendar.objects.get(date=due_date)
        if due_date.day_no == 'H':
            raise forms.ValidationError("Can't be due on a holiday")
        
        return due_date
        
#     def clean_class_db(self):
#         class_db=self.cleaned_data['class_db']
#         if not self.request.user.is_staff:
#             inclass=self.request.user.get_profile().in_class.classes
#             for i in range(len(class_db)):
#                 if class_db[i].classes != inclass:
#                     raise forms.ValidationError("You can only add homework to your class.")
#         return class_db
