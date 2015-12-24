from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, FormView
from classsite.views import URLMixin
from kalendar.models import Kalendar, Day_No
from classlists.models import Klass
from .models import Period_Details, Period_Activity, Period_ActivityForm, Day_ActivityForm
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from django.forms import formset_factory

#Finds Monday for that week, if weekend finds next monday
def get_monday():
    if date.today().weekday()<5:
        monday=date.today()+timedelta(days=-(date.today().weekday()))
    else:
        monday=date.today()+timedelta(days=+(7-date.today().weekday()))
        
    return monday

class ScheduleView(URLMixin, TemplateView):
	template_name='schedule/schedule.html'
	
	def get_context_data(self, **kwargs):
	
	    context=super(ScheduleView, self).get_context_data(**kwargs)
	    klass=get_object_or_404(Klass,name=self.kwargs['class_url'])
	    setup=klass.schedule
	    periods_in_day=setup.periods_in_day
	    periods=[None]*periods_in_day
	    
	    ##gets days of weeks
	    monday=get_monday()
	    week=[]
	    week.append(Kalendar.objects.get(date=monday))
	    
	    #Finds kalendar object for Tuesday to Friday
	    for i in range(1,5):
	        week.append(Kalendar.objects.get(id=(week[0].id+i)))
	    
	    friday=week[4].date 
	    
	    ##clean up non-permanents from last week
	    Period_Activity.objects.filter(org=False, org_date__lt=monday).delete()
	    
	    for p in range(periods_in_day):
	        per_detail=Period_Details.objects.get(setup=setup, number=p+1)
	        per_activity=[]
	        for i in range(5):   
	            ##gets period_activities for klass, details and day_no and if org_date is on or before Friday of this week 
	            per_activity.append((Period_Activity.objects.get(klass=klass, details=per_detail, day_no=week[i].day_no, org_date__lte=friday),week[i].day_no))
	        periods[p]=(per_detail, per_activity)

	    context['week']=week
	    context['periods']=periods
	    return context

class ActivityUpdateView(URLMixin, UpdateView):
    form_class=Period_ActivityForm
    model=Period_Activity
    template_name='generic/generic_only_modify2.html'
    title='Activity'

    def form_valid(self, form):
        new_activity=form.save(commit=False)
        perm=form.cleaned_data['permanent']
        
        org_activity=Period_Activity.objects.get(pk=self.kwargs['pk'])
        
        ## Perm to Perm and Temp to Temp taken care of with simple save
        
        ## Perm to Temp
        if not perm and org_activity.org==True:
            
            ##date should be Monday of next week
            next_monday=get_monday()
            if next_monday < date.today():
                next_monday=next_monday+timedelta(days=+7)
            org_activity.org_date=next_monday
            org_activity.save()
            
            new_activity.pk=None
            new_activity.org=False
            new_activity.org_date=date.today()
    
        ## what happens if make non-perm to permanent change
    
        new_activity.save()

        return HttpResponseRedirect(reverse('schedule-view', args=(self.kwargs['class_url'],)))

class ActivityDayUpdateView(URLMixin, FormView):
    form_class=Day_ActivityForm
    template_name='schedule/activity_day_update_form.html'

    def get_form_class(self):
        klass=Klass.objects.get(name=self.kwargs['class_url'])
        extra=klass.schedule.periods_in_day
        return formset_factory(Day_ActivityForm, extra=extra)

    def get_context_data(self, **kwargs):
        context=super(ActivityDayUpdateView, self).get_context_data(**kwargs)

        setup=context['klass'].schedule
        period_details=Period_Details.objects.filter(setup=setup)

        formset=context['form']
        context['formset']=formset

        form_with_details=zip(period_details, formset)
        context['form_with_details']=form_with_details
        
        #not neccessary find the actual object
        context['day_no']=Day_No.objects.get(day_name=self.kwargs['dayno_pk'])
        return context

    def form_valid(self, form):
        klass=Klass.objects.get(name=self.kwargs['class_url'])
        day_no=Day_No.objects.get(day_name=self.kwargs['dayno_pk'])
        setup=klass.schedule
        i=0
        for f in form:
            i+=1
            details=Period_Details.objects.get(setup=setup,number=i)
            new_activity=Period_Activity.objects.get(day_no=day_no,details=details)
            form_activity=f.save(commit=False)
            new_activity.activity=form_activity.activity
            new_activity.save()
 
        return HttpResponseRedirect(reverse('schedule-view', args=(self.kwargs['class_url'],)))
           