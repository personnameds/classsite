from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from kalendar.models import Kalendar, Update_Day_No_Kalendar_Form, Event, Add_Event_Form 
from classlists.models import Klass
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView

from datetime import date, timedelta
 

class EventCreateView(CreateView):
 	model=Event
 	form_class=Add_Event_Form
 
 	def get_context_data(self, **kwargs):
 	    context=super(EventCreateView, self).get_context_data(**kwargs)
 	    context['event_date']=date(int(self.kwargs['year']),int(self.kwargs['month']),int(self.kwargs['day']))	
 	    context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
 	    context['path']=self.request.path
 	    context['kal_type']=self.kwargs['kal_type']
 	    return context

   	def form_valid(self, form):
 		
 		klass=self.kwargs['class_url']
 		kal_type=self.kwargs['kal_type']
 		
 		event_date=date(int(self.kwargs['year']),int(self.kwargs['month']),int(self.kwargs['day']))
 		new_event=form.save(commit=True)
 		new_event.event_date=Kalendar.objects.get(date=event_date)
 		if new_event.kksa:
 		    for k in Klass.objects.all():
 		        new_event.klass.add(k)
 		    new_event.save()
 		else:
 		    new_event.save()
 		
 		return HttpResponseRedirect(reverse('kalendar_view', args=(klass, kal_type, event_date.year,event_date.month)))



class EventUpdateView(UpdateView):
    model=Event
    form_class=Add_Event_Form
    template_name="kalendar/modify_event.html"

    def get_context_data(self, **kwargs):
 	    context=super(EventUpdateView, self).get_context_data(**kwargs)
 	    context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
 	    context['path']=self.request.path
 	    context['kal_type']=self.kwargs['kal_type']
 	    return context
 	
 	
    def get_initial(self, **kwargs):
	    initial=super(EventUpdateView, self).get_initial()
	    pk=self.kwargs['pk']
	    initial['event_date']=Event.objects.get(id=pk).event_date
	    return initial
    
    def form_valid(self, form):
        klass=self.kwargs['class_url']
        kal_type=self.kwargs['kal_type'] 		
        
        pk=self.kwargs['pk']
        new_event=Event.objects.get(id=pk)
        event_date=new_event.event_date
        if self.request.POST['mod/del']=='Delete':
            new_event.delete()
        else:
            new_homepage=form.save()
        return HttpResponseRedirect(reverse('kalendar_view', args=(klass, kal_type, event_date.date.year,event_date.date.month)))     


class KalendarListView(ListView):
    template_name="kalendar/kalendar_list.html"
    context_object_name='kalendar_list'

    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        kal_type=self.kwargs['kal_type']
        context=super(KalendarListView, self).get_context_data(**kwargs)
        
        
        context['kal_type']=kal_type
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['path']=self.request.path

        #first, last of entire kalendar dates and current viewing date
        month=int(self.kwargs.get('month', date.today().month))
        year=int(self.kwargs.get('year', date.today().year))
        firstest_date=Kalendar.objects.all().order_by('date')[0].date
        lastest_date=Kalendar.objects.all().order_by('-date')[0].date
        viewing_date=date(year,month,1)

        
        
        #code to add blank inserts only for very first month and very last month
        insert_counter=0
        if viewing_date.month == firstest_date.month:
            if viewing_date.weekday() > 0 and viewing_date.weekday() < 5:
                insert_counter=viewing_date.weekday()

        #can't loop over an integer in template so this creates a list of that number
        context['insert_counter']=[i+1 for i in range(insert_counter)]

        context['firstest_date']=firstest_date
        context['lastest_date']=lastest_date       
        context['viewing_date']=viewing_date
        return context

    def get_queryset(self):
                
        month=int(self.kwargs.get('month', date.today().month))
        year=int(self.kwargs.get('year', date.today().year))
        
        first_date=date(year,month,1)
        
        #only gets weekdays of the month being viewed
        #finds first weekday of month
        if first_date.weekday() < 5:
            first_kal_date=first_date+timedelta(days=-first_date.weekday())
        else:
            first_kal_date=first_date+timedelta(days=+(7-first_date.weekday()))
        #finds last day of month
        if month !=12:
            last_date=date(year,(month+1),1)-timedelta(days=1)
        else:
            last_date=date(year,12,31)
        #finds last weekday of month
        if last_date.weekday() < 5:
            last_kal_date=last_date+timedelta(days=+(4-last_date.weekday()))
        else:
            last_kal_date=last_date+timedelta(days=-(last_date.weekday()-4))
	
        return Kalendar.objects.filter(date__gte=first_kal_date, 
                                       date__lte=last_kal_date,
                                       ).order_by('date')





class UpdateDayNoKalendarView(UpdateView):
    form_class=Update_Day_No_Kalendar_Form
    model=Kalendar
    template_name='kalendar/modify_kalendar_form.html'
    
    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(UpdateDayNoKalendarView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['path']=self.request.path
        return context
    
    def get_object(self):
        object=super(UpdateDayNoKalendarView, self).get_object()
        return object
        
    def form_valid(self, form):
    
	    klass=self.kwargs['class_url']
	    kal_type=self.kwargs['kal_type']
	    
	    new_kalendar_object=form.save(commit=False)
	    new_day_no=new_kalendar_object.day_no
	    date_to_change=new_kalendar_object.date
	    kal_to_change=Kalendar.objects.get(date=date_to_change)
	    id_to_change=kal_to_change.id
	    
	    ##make first change to kalendar
	    
	    ##change from # to H
	    if (kal_to_change.day_no != 'H') and (new_day_no == 'H'):
	        pre_day_no=kal_to_change.day_no
	        changed_day=Kalendar(id=id_to_change, date=kal_to_change.date, day_no=new_day_no)
	        changed_day.save()
	        new_day_no=pre_day_no
	    
	    ##change from # to #
	    elif (kal_to_change.day_no != 'H') and (new_day_no != 'H'):
	        changed_day=Kalendar(id=id_to_change, date=kal_to_change.date, day_no=new_day_no)
	        changed_day.save()
	        
	        if new_day_no == '5':
	            new_day_no = '1'
	        else:
	            new_day_no = str(int(new_day_no)+1)
	        
	    ##change from H to #
	    elif (kal_to_change.day_no == 'H') and (new_day_no != 'H'):
	        changed_day=Kalendar(id=id_to_change, date=kal_to_change.date, day_no=new_day_no)
	        changed_day.save()
	        if new_day_no == '5':
	            new_day_no = '1'
	        else:
	            new_day_no = str(int(new_day_no)+1)
	            
	    ##change from H to H
	    elif (kal_to_change.day_no == 'H') and (new_day_no == 'H'):
	        changed_day=Kalendar(id=id_to_change, date=kal_to_change.date, day_no=new_day_no)
	        changed_day.save()
	        new_day_no=False
	        
	    ##rest of kalendar
	    if new_day_no:
	        for	k in Kalendar.objects.filter(date__gt=date_to_change).iterator():
	            ##check if day being changed is H
	            if k.day_no == 'H':
	                ##makes no changes
	                pass
	            
	            ##if a day 1 to 5 changes the day number and then updates new day to the next day number
	            elif k.day_no != 'H':
	                changed_day=Kalendar(id=k.id, date=k.date, day_no=new_day_no)
	                changed_day.save()
	                
	                if new_day_no == '5':
	                    new_day_no = '1'
	                else:
	                    new_day_no = str(int(new_day_no)+1)
	    return HttpResponseRedirect(reverse('kalendar_view', args=(klass, kal_type, new_kalendar_object.date.year,new_kalendar_object.date.month)))
