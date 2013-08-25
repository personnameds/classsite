# from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
# from django.core.urlresolvers import reverse_lazy
# from django.template import RequestContext
# from kalendar.models import Kalendar, Update_Day_No_Kalendar_Form, Event, Add_Event_Form 
# from day_no.models import Day_No
# from classlists.models import Classes
# from django.views.generic.edit import UpdateView, CreateView
# from django.views.generic import ListView

#from datetime import date, timedelta
 

class EventCreateView(CreateView):
 	model=Event
 	form_class=Add_Event_Form
 
 	def get_context_data(self, **kwargs):
 		context=super(EventCreateView, self).get_context_data(**kwargs)
 		context['event_date']=date(int(self.kwargs['year']),int(self.kwargs['month']),int(self.kwargs['day']))	
 		class_url=self.kwargs['class_url']
 		context['class_url']=class_url.lower()
 		return context

   	def form_valid(self, form):
 		event_date=date(int(self.kwargs['year']),int(self.kwargs['month']),int(self.kwargs['day']))
 		new_event=form.save(commit=False)
 		new_event.event_date=Kalendar.objects.get(date=event_date)
 		new_event.save()
 		form.save_m2m()
 		return HttpResponseRedirect(reverse_lazy('kal-list-view', args=(self.kwargs['class_url'],int(self.kwargs['year']),int(self.kwargs['month']),)))

class EventUpdateView(UpdateView):
    model=Event
    form_class=Add_Event_Form
    template_name="kalendar/modify_event.html"

    def get_context_data(self, **kwargs):
        class_url=self.kwargs['class_url']
        context=super(EventUpdateView, self).get_context_data(**kwargs)
        context['class_url']=class_url.lower()
        return context
    
	def get_initial(self, **kwargs):
	    initial=super(EventUpdateView, self).get_initial()
	    pk=self.kwargs['pk']
	    initial['event_date']=Event.objects.get(id=pk).event_date
	    return initial
    
    def form_valid(self, form):
        pk=self.kwargs['pk']
        new_event=Event.objects.get(id=pk)
        if self.request.POST['mod/del']=='Delete':
            new_event.delete()
            return HttpResponseRedirect(reverse_lazy('kal-list-view', args=(self.kwargs['class_url'],new_event.event_date.date.year,new_event.event_date.date.month),))
        else:
            new_homepage=form.save()
            return HttpResponseRedirect(reverse_lazy('kal-list-view', args=(self.kwargs['class_url'],new_event.event_date.date.year,new_event.event_date.date.month),))
            




class KalendarListView(ListView):
    template_name="kalendar/kalendar_list.html"

    def get_queryset(self):
        
        class_db=Classes.objects.get(classes=self.kwargs['class_url'])
        
        try:
            month=int(self.kwargs['month'])
            year=int(self.kwargs['year'])
        except:
            month=date.today().month
            year=date.today().year

        first_date=date(year,month,1)
        
        
        if first_date.weekday() < 5:
            first_kal_date=first_date+timedelta(days=-first_date.weekday())
        else:
            first_kal_date=first_date+timedelta(days=+(7-first_date.weekday()))

        if month !=12:
            last_date=date(year,(month+1),1)-timedelta(days=1)
        else:
            last_date=date(year,12,31)
            
        if last_date.weekday() < 5:
            last_kal_date=last_date+timedelta(days=+(4-last_date.weekday()))
        else:
            last_kal_date=last_date+timedelta(days=-(last_date.weekday()-4))
	
        return Kalendar.objects.filter(date__gte=first_kal_date, date__lte=last_kal_date)
   
    def get_context_data(self, **kwargs):
        ##repetitive code in get_quertyset and get_context_data
        
        try:
            month=int(self.kwargs['month'])
            year=int(self.kwargs['year'])
        except:
            month=date.today().month
            year=date.today().year

        first_date=date(year,month,1)
        
        ##end of repetitive code
        

        class_url=self.kwargs['class_url']
        class_db=Classes.objects.get(classes=self.kwargs['class_url'])
        context=super(KalendarListView, self).get_context_data(**kwargs)
        context['class_url']=class_url.lower()
        
        viewing_date=date(year,month,1)
        
        Q=Kalendar.objects.all()
        last=Q.count()
        firstest_date=Q.get(pk=1).date
        lastest_date=Q.get(pk=last).date
        
        if first_date.weekday() < 5:
            first_kal_date=first_date+timedelta(days=-first_date.weekday())
        else:
            first_kal_date=first_date+timedelta(days=+(7-first_date.weekday()))
        
        context['viewing_date']=viewing_date
        context['firstest_date']=firstest_date
        context['lastest_date']=lastest_date
        
        insert_counter=[]
        if viewing_date.month==firstest_date.month:
            insert_dates=firstest_date-first_kal_date
            
            if insert_dates.days > 4:
                insert_dates=insert_dates.days-7
            else:
                insert_dates=insert_dates.days
            
            if insert_dates > 0:
                for i in range(insert_dates):
                    insert_counter.append(i)

        context['insert_counter']=insert_counter
        
        return context

class UpdateDayNoKalendarView(UpdateView):
	form_class=Update_Day_No_Kalendar_Form
	model=Kalendar
	template_name='kalendar/modify_kalendar_form.html'
	
	def get_context_data(self, **kwargs):
	    class_url=self.kwargs['class_url']
	    context=super(UpdateDayNoKalendarView, self).get_context_data(**kwargs)
	    context['class_url']=class_url.lower()
	    return context
	
	def get_object(self):
		object=super(UpdateDayNoKalendarView, self).get_object()
		return object
		
	def form_valid(self, form):
		
		class_url=self.kwargs['class_url']
		
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


		return HttpResponseRedirect(reverse_lazy('kal-list-view', args=(class_url, new_kalendar_object.date.year,new_kalendar_object.date.month)))
