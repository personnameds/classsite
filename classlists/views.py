from classlists.models import ClassesForm, Classes
from day_no.models import Day_No
from django.views.generic.edit import CreateView

class AddClassCreateView(CreateView):
    template_name='classlists/add_class_form.html'
    form_class=ClassesForm

    def get_success_url(self):
	    day_list=('1P','2P','3P','4P','5P','HP','1M','2M','3M','4M','5M','HM')
	    
	    for i in day_list:
		    new_day_no=Day_No(
			    day_no=i,
			    before_event="",
			    period1_event="P1",			
			    period2_event="P2",				
			    period3_event="P3",				
			    lunch_event="Lunch",
			    period4_event="P4",				
			    period5_event="P5",			
			    period6_event="P6",						
			    after_event="",	
			    class_db=self.object,
			    )
		    new_day_no.save()
