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
	    Period_Activity.objects.filter(org=False, del_date__lt=monday).delete()

	    for p in range(periods_in_day):
	        per_detail=Period_Details.objects.get(setup=setup, number=p+1)
	        per_activity=[]
	        for i in range(5):   
	            ##gets period_activities for klass, details and day_no and if org_date is on or before Friday of this week 
	            a=klass
	            b=per_detail
	            c=week[i].day_no
	            d=del_date__lte=friday
	            z=Period_Activity.objects.get(klass=klass, details=per_detail, day_no=week[i].day_no, del_date__lte=friday)
	            per_activity.append((Period_Activity.objects.get(klass=klass, details=per_detail, day_no=week[i].day_no, del_date__lte=friday),week[i].day_no))
	        periods[p]=(per_detail, per_activity)

	    context['week']=week
	    context['periods']=periods
	    return context

class ActivityUpdateView(URLMixin, UpdateView):
    form_class=Period_ActivityForm
    model=Period_Activity
    template_name='schedule/activity_period_update_form.html'
    title='Activity'

    def form_valid(self, form):
        new_activity=form.save(commit=False)
        perm=self.request.POST['temp/perm']
        
        old_activity=Period_Activity.objects.get(pk=self.kwargs['pk'])
        ## Perm to Perm and Temp to Temp taken care of with simple save
        
        ## Perm to Temp
        if perm=='This Week' and old_activity.org==True:
            
            ##date should be Monday of next week
            next_monday=get_monday()+timedelta(days=+7)
            old_activity.del_date=next_monday
            old_activity.save()
            
            new_activity.pk=None
            new_activity.org=False
            if date.today().weekday()<5:
                new_activity.del_date=date.today()
            else:
                new_activity.del_date=get_monday()
    
        ## Temp to Perm
        if perm=='Permanent' and old_activity.org==False:
            old_org_activity=Period_Activity.objects.get(details=old_activity.details, day_no=old_activity.day_no, org=True)
            old_org_activity.delete()
            new_activity.org=True
            new_activity.del_date=date.today()
        
        ##Saves new activity regardless of choice
        new_activity.save()

        return HttpResponseRedirect(reverse('schedule-view', args=(self.kwargs['class_url'],)))

class ActivityDayUpdateView(URLMixin, FormView):
    form_class=Day_ActivityForm
    template_name='schedule/activity_day_update_form.html'

        #self.fields['permanent']=BooleanField(label='Permanent Change',required=False)

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
            form_activity=f.save(commit=False)
            if form_activity.activity != '':
                Period_Activity.objects.filter(org=False, day_no=day_no, details=details, klass=klass).delete()
                new_activity=Period_Activity.objects.get(day_no=day_no,details=details,klass=klass)
                new_activity.activity=form_activity.activity
                new_activity.del_date=date.today()
                new_activity.save()
 
        return HttpResponseRedirect(reverse('schedule-view', args=(self.kwargs['class_url'],)))
           