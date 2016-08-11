from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView
from classsite.views import URLMixin, SchoolNameMixin
from .models import Kalendar, Day_No, Kalendar_Setup, Change_Day_NoForm, Event_Form, Event
from datetime import date, timedelta
from classlists.models import Klass 
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

class KalendarListView(URLMixin, ListView): 
    template_name="kalendar/kalendar_list.html"
    context_object_name='combo_list'
    model=Kalendar
    
    def get_queryset(self):
        klass=get_object_or_404(Klass,name=self.kwargs['class_url'])
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
        
        kalendar_list=Kalendar.objects.filter(date__gte=first_kal_date, date__lte=last_kal_date,).order_by('date')
        
        combo_list=[]
        for k in kalendar_list:
            combo_list.append((k,k.event_set.filter(klass=klass),k.hwk_details_set.filter(klass=klass)))
        return combo_list  
    
    def get_context_data(self, **kwargs):
        context=super(KalendarListView, self).get_context_data(**kwargs)
        month=int(self.kwargs.get('month', date.today().month))
        year=int(self.kwargs.get('year', date.today().year))
        
        kal_total_list=Kalendar.objects.all().order_by('date')
        firstest_date=kal_total_list.first().date
        lastest_date=kal_total_list.last().date
        viewing_date=date(year,month,1)
        
        insert_counter=0
        if viewing_date.month == firstest_date.month:
            if viewing_date.weekday() > 0 and viewing_date.weekday() < 5:
                insert_counter=viewing_date.weekday()
            
        #can't loop over an integer in template so this creates a list of that number
        context['insert_counter']=[i+1 for i in range(insert_counter)]

        context['firstest_date']=firstest_date
        context['lastest_date']=lastest_date       
        context['viewing_date']=viewing_date
        
        if month != 12:
            context['next_month']=month+1
            context['next_year']=year
        else:
            context['next_month']=1
            context['next_year']=year+1
        if month != 1:
            context['prev_month']=month-1
            context['prev_year']=year
        else:
            context['prev_month']=12
            context['prev_year']=year-1
            
        return context

class SchoolKalendarTemplateView(URLMixin, SchoolNameMixin, TemplateView): 
    template_name="kalendar/school_kalendar.html"


class DayNoUpdateView(URLMixin, UpdateView):
    form_class=Change_Day_NoForm
    model=Kalendar
    template_name='generic/generic_only_modify.html'
    title='Day Number'
    named_url='dayno-update-view'
    
    def get_initial(self, **kwargs):
        initial=super(DayNoUpdateView, self).get_initial()
        
        initial['date_from']=self.object
        initial['date_until']=self.object
        return initial
    
    def form_valid(self, form):
    
	    date_from=form.cleaned_data['date_from']
	    date_until=form.cleaned_data['date_until']
	    date_range=Kalendar.objects.filter(date__range=(date_from.date, date_until.date))

	    old_dayno=date_from.day_no
	    new_dayno=form.cleaned_data['day_no']
	    
	    total_daynos=Kalendar_Setup.objects.get(name=settings.SCHOOL).days_in_cycle
	    day=[None]*(total_daynos+1)
	    day[0]=Day_No.objects.get(day_name='H')
	    for i in range(1,total_daynos+1):
	        day[i]=Day_No.objects.get(day_name=str(i))
	    
	    for j in date_range:
	        j.day_no=new_dayno
	        j.save()
	    
        ##Find the day number for the next day so that the calendar can be updated
	    ##change from # to H
	    if (old_dayno != day[0]) and (new_dayno == day[0]):
	        next_dayno=old_dayno
	        
	    ##change from # to # or from H to #
	    elif new_dayno != day[0]:
	        if new_dayno == day[total_daynos]:
	            next_dayno = day[1]
	        else:
	            next_dayno = day[int(new_dayno.day_name)+1]
	    
	    ##change from H to H
	    elif (old_dayno == day[0]) and (new_dayno == day[0]):
	        next_dayno=False
	        
	        
	    ##Recreates rest of calendar
	    if next_dayno:
	        for	k in Kalendar.objects.filter(date__gt=date_until.date).iterator():
	            ##check if day being changed is H
	            if k.day_no == day[0]:
	                pass
	                
	            ##if a day 1 to 5 changes the day number and then updates new day to the next day number
	            elif k.day_no != day[0]:
	                k.day_no=next_dayno
	                k.save()

	                if next_dayno == day[total_daynos]:
	                    next_dayno = day[1]
	                else:
	                    next_dayno = day[int(next_dayno.day_name)+1]
	                    
	    return HttpResponseRedirect(reverse('kalendar-view', args=(self.kwargs['class_url'],date_from.date.year,date_from.date.month)))

class EventCreateView(URLMixin, CreateView):
    form_class=Event_Form
    model=Event
    template_name='generic/generic_form2.html'
    title='Event'
    named_url='event-create-view'

    def get_initial(self, **kwargs):
        initial=super(EventCreateView, self).get_initial()
        initial['klass']=Klass.objects.filter(name=self.kwargs['class_url'])
        return initial

    def form_valid(self, form):
        new_event=form.save(commit=False)
        new_event.event_date=Kalendar.objects.get(pk=self.kwargs['pk'])
        new_event.save()
        for klass in form.cleaned_data['klass']:
            new_event.klass.add(klass)
            
        return HttpResponseRedirect(reverse('kalendar-view', args=(self.kwargs['class_url'],new_event.event_date.date.year,new_event.event_date.date.month)))

class EventUpdateView(URLMixin, UpdateView):
    form_class=Event_Form
    model=Event
    template_name='generic/generic_modify.html'
    title='Event'
    named_url='event-update-view'

    def form_valid(self, form):
    
        if self.request.POST['mod/del'] == 'Delete':
            del_event=self.object
            for klass in form.cleaned_data['klass']:
                del_event.klass.remove(klass)
            if del_event.klass.all().count()==0:
                del_event.delete()
        
        else:
            new_event=form.save(commit=False)
            new_event.event_date=Kalendar.objects.get(pk=self.kwargs['pk'])
            new_event.save()
            for klass in form.cleaned_data['klass']:
                new_event.klass.add(klass)
            
        return HttpResponseRedirect(reverse('kalendar-view', args=(self.kwargs['class_url'],self.object.event_date.date.year,self.object.event_date.date.month)))
