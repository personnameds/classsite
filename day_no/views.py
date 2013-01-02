from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import UpdateView
from day_no.models import Day_No, Add_Day_No_Form
from classlists.models import Classes
from kalendar.models import Kalendar
from django.core.urlresolvers import reverse_lazy
from datetime import time

class UpdateDayNoView(UpdateView):
	model=Day_No
	form_class=Add_Day_No_Form
	
	def get_context_data(self, **kwargs):
	    class_url=self.kwargs['class_url']
	    context=super(UpdateDayNoView, self).get_context_data(**kwargs)
	    context['class_url']=class_url.lower()
	    context['day_no_text']=Day_No.objects.get(pk=self.kwargs['pk']).day_no[0]
	    return context

	def get_form_kwargs(self):
	    kwargs=super(UpdateDayNoView, self).get_form_kwargs()
	    kwargs.update({'request':self.request, 'class_url':self.kwargs['class_url']})
	    return kwargs
	    
	def form_valid(self, form):
	    class_db=Classes.objects.get(classes=self.kwargs['class_url'])
	    change_type=self.request.POST['change_type']
	    
	    #first change the day_no if it is P or M
	    mod_dayno=form.save(commit=False)
	    mod_day_name=mod_dayno.day_no[0]+change_type
	    mod_day_id=Day_No.objects.filter(class_db=class_db).get(day_no=mod_day_name)
	    mod_dayno.id=mod_day_id.id
	    mod_dayno.day_no=mod_day_name
	    mod_dayno.save()
	    
	    #if it is P then also change the M day_no to match it
	    if change_type=='P':
	        mod_day_name=mod_dayno.day_no[0]+'M'
	        mod_day_id=Day_No.objects.filter(class_db=class_db).get(day_no=mod_day_name)
	        mod_dayno.id=mod_day_id.id
	        mod_dayno.day_no=mod_day_name
	        mod_dayno.save()
	    
	    #always adding the M to day_version
	    kid=int(self.kwargs['kid'])
	    k=Kalendar.objects.get(id=kid)
	    k.day_version.add(mod_dayno)
	        
	    return HttpResponseRedirect(reverse_lazy('schedule-template-view', args=(self.kwargs['class_url'],)))
