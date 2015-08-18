from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput, Textarea
from messages.models import Topic, Msg
from homework.models import Hwk_Details
from datetime import date, timedelta
        
class Add_Topic_Form(ModelForm):

    hwk_details=forms.ModelChoiceField(
            queryset=Hwk_Details.objects.exclude(due_date__date__lt=(date.today())),
            label='Applies to:',
            required=False,
            )
    
    class Meta:
		model=Topic
		widgets={
			'description':TextInput(attrs={'size':'45'}),
			}
		fields=['topic']


class Add_Message_Form(ModelForm):
	class Meta:
		model=Msg
		widgets={
			'msg_text':Textarea(),
			}
		fields=['msg_text',]
