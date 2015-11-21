from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView ##, FormView
from classsite.views import URLMixin
from kalendar.models import Kalendar, Day_No
from classlists.models import Klass
from .models import Period_Details, Period_Activity, Period_ActivityForm
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
##from django.forms import formset_factory

class ScheduleView(URLMixin, TemplateView):
	template_name='schedule/schedule.html'
	
	def get_context_data(self, **kwargs):
	
	    context=super(ScheduleView, self).get_context_data(**kwargs)
	    klass=get_object_or_404(Klass,name=self.kwargs['class_url'])
	    setup=klass.schedule
	    periods_in_day=setup.periods_in_day
	    periods=[None]*periods_in_day
	    
	    #Finds Monday for that week, if weekend finds next monday
	    week=[]
	    if date.today().weekday() <5:
	        monday=date.today()+timedelta(days=-(date.today().weekday()))
	    else:
	        monday=date.today()+timedelta(days=+(7-date.today().weekday()))
	    week.append(Kalendar.objects.get(date=monday))
	    
	    #Finds kalendar object for Tuesday to Friday
	    for i in range(1,5):
	        week.append(Kalendar.objects.get(id=(week[0].id+i)))
	        
	    for p in range(periods_in_day):
	        per_detail=Period_Details.objects.get(setup=setup, number=p+1)
	        per_activity=[]
	        for i in range(5):    
	            ##Use filter so don't get 404 if Activity not setup
	            ##Creates a messy hack in template
	            per_activity.append((Period_Activity.objects.filter(klass=klass, details=per_detail, day_no=week[i].day_no),week[i].day_no))
	        periods[p]=(per_detail, per_activity)

	    context['week']=week
	    context['periods']=periods
	    return context

class ActivityCreateView(URLMixin, CreateView):
    form_class=Period_ActivityForm
    model=Period_Activity
    template_name='generic/generic_form2.html'
    title='Activity'

    def form_valid(self, form):
        new_activity=form.save(commit=False)
        period_detail=Period_Details.objects.get(pk=self.kwargs['perdet_pk'])
        day_no=Day_No.objects.get(pk=self.kwargs['dayno_pk'])
        klass=Klass.objects.get(name=self.kwargs['class_url'])
        new_activity.klass=klass
        new_activity.org=True
        new_activity.org_date=date.today()
        new_activity.details=period_detail
        new_activity.day_no=day_no
        new_activity.save()

        return HttpResponseRedirect(reverse('schedule-view', args=(self.kwargs['class_url'],)))

class ActivityUpdateView(URLMixin, UpdateView):
    form_class=Period_ActivityForm
    model=Period_Activity
    template_name='generic/generic_form2.html'
    title='Activity'

    def form_valid(self, form):
        new_activity=form.save(commit=False)
        new_activity.save()

        return HttpResponseRedirect(reverse('schedule-view', args=(self.kwargs['class_url'],)))

# class ActivityDayUpdateView(URLMixin, FormView):
#     template_name='schedule/activity_day_update_form.html'
#     
#     def get_form_class(self):
#         klass=Klass.objects.get(name=self.kwargs['class_url'])
#         extra=klass.schedule.periods_in_day
#         return formset_factory(Period_ActivityForm, extra=extra)
# 
#     def form_valid(self, form):
#         a=z
#         setup=Schedule_Setup.objects.get(pk=self.kwargs['setup_id'])
#         period_num=0
#         for f in form:
#             period_num+=1
#             per_detail=f.save(commit=False)
#             per_detail.number=period_num
#             per_detail.setup=setup
#             per_detail.save()
# 
#         return HttpResponseRedirect(reverse('schedule-setup-view',))
