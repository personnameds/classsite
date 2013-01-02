from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from kalendar.models import Kalendar
from day_no.models import Day_No
from classlists.models import Classes

from datetime import date, timedelta

class ScheduleTemplateView(TemplateView):
	template_name='schedule/schedule.html'
	
	def get_context_data(self, **kwargs):

		class_url=self.kwargs['class_url']
		class_db=Classes.objects.get(classes=class_url)
		
		week=[0]*5
		days=[0]*5
		
		if date.today().weekday() <5:
			monday=date.today()+timedelta(days=-(date.today().weekday()))
		else:
			monday=date.today()+timedelta(days=+(7-date.today().weekday()))
		week[0]=Kalendar.objects.get(date=monday)
		
		for i in range(1,5):
			week[i]=Kalendar.objects.get(id=(week[0].id+i))
		
		q=Day_No.objects.filter(class_db=class_db)
		for i in range(0,5):
		    if week[i].day_version.filter(class_db=class_db):
		        days[i]=week[i].day_version.get(class_db=class_db)
		    else:
		        days[i]=q.get(day_no=week[i].day_no+'P')
		    
		list=zip(days, week)
		    
		context=super(ScheduleTemplateView, self).get_context_data(**kwargs)
		context['week']=week
		context['days']=days
		context['list']=list

		context['class_url']=class_url.lower()
		
		return context
