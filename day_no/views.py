from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from day_no.models import Day_No, Update_Day_No_Form
from classlists.models import Klass
from kalendar.models import Kalendar
from django.core.urlresolvers import reverse
from datetime import time

class UpdateDayNoView(UpdateView):
	model=Day_No
	form_class=Update_Day_No_Form
	
	def get_context_data(self, **kwargs):
	    context=super(UpdateDayNoView, self).get_context_data(**kwargs)
	    context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    context['path']=self.request.path
	    context['day_no_text']=Day_No.objects.get(pk=self.kwargs['pk']).day_name[0]
	    return context
	
	def get_initial(self, **kwargs):
	    initial=super(UpdateDayNoView, self).get_initial()
	    initial['mod_for_date']=Kalendar.objects.get(id=self.kwargs['kid'])
	
	def form_valid(self, form):
	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    change_type=self.request.POST['change_type']
	    
	    mod_day=form.save(commit=False)
	    #first change the day_name if it is P or M
	    mod_day.day_name=mod_day.day_name[0]+change_type
	    mod_day.id=Day_No.objects.filter(klass=klass).get(day_name=mod_day.day_name).id
	    mod_day.save()
	    
	    #if change is P then also change M
	    if change_type=='P':
	        mod_day.day_name=mod_day.day_name[0]+'M'
	        mod_day.id=Day_No.objects.filter(klass=klass).get(day_name=mod_day.day_name).id
	        mod_day.save()  
	    
	    #add to day_version
	    kid=int(self.kwargs['kid'])
	    k=Kalendar.objects.get(id=kid)
	    k.day_version.add(mod_day)
	    
	    return HttpResponseRedirect(reverse('schedule_view', args=(self.kwargs['class_url'],)))