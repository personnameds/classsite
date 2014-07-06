from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from homework.models import Homework, Homework_Form
from classlists.models import Klass, KKSA_Staff
from kalendar.models import Kalendar
from datetime import datetime, date, timedelta
from django.core.urlresolvers import reverse


class HomeworkListView(ListView):
    template_name="homework_list.html"
    
    def get_queryset(self):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        return Homework.objects.all().exclude(due_date__date__lt=(date.today())).filter(klass__id=klass.id)
        
    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(HomeworkListView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['next']=self.request.path
        context['now']=datetime.now()
        return context


class HomeworkCreateView(CreateView):
    model=Homework
    form_class=Homework_Form
    template_name="homework/homework_form.html"
    
    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(HomeworkCreateView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['next']=self.request.path
        return context
    
    def get_initial(self, **kwargs):
        initial=super(HomeworkCreateView, self).get_initial()
        klass=self.kwargs['class_url']
        klass=Klass.objects.filter(klass_name=self.kwargs['class_url'])
        initial['klass']=klass
        return initial
    
    #Choose Klass field only available for teachers
    def get_form(self, form_class):
        form=super(HomeworkCreateView, self).get_form(form_class)
        if not self.request.user.has_perm('classlists.is_kksastaff'):
            form.fields.pop('klass')
        return form

    def form_valid(self, form):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        new_homework=form.save(commit=False)
        new_homework.entered_by=self.request.user
        new_homework.entered_on=datetime.today()
        new_homework.deleted=False
        new_homework.save()
        new_homework.klass.add(klass)
        form.save_m2m()
        
        return HttpResponseRedirect(reverse('homework_view', args=(self.kwargs['class_url'],),))


class HomeworkUpdateView(UpdateView):
    model=Homework
    form_class=Homework_Form
    template_name="homework/modify_homework.html"

    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context=super(HomeworkUpdateView, self).get_context_data(**kwargs)
        context['klass']=klass
        context['next']=self.request.path
        return context
    
    #Choose Klass field only available for teachers
    def get_form(self, form_class):
        form=super(HomeworkUpdateView, self).get_form(form_class)
        if not self.request.user.has_perm('classlists.is_kksastaff'):
            form.fields.pop('klass')
        return form

    def form_valid(self, form):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        
        #Delete homework
        if self.request.POST['mod/del']=='Delete':
            #If Teacher
            if self.request.user.has_perm('classlists.is_kksastaff'):
                del_homework=form.save(commit=False)
                for k in form.cleaned_data['klass']:
                    del_homework.klass.remove(k)
                if del_homework.klass.count()==0:
                    del_homework.delete()
            #if not a teacher
            else: 
                if h.klass.count() > 1: #if more than 1 class attached to homework
                    pass ##need to erase 1 class but keep the other classes untouched
                else: #if only 1 class set deleted to True
                    del_homework=form.save(commit=False)
                    del_homework.modified_by=self.request.user
                    del_homework.modified_on=datetime.today()
                    del_homework.deleted=True
                    del_homework.save()
            return HttpResponseRedirect(reverse('homework_view', args=(self.kwargs['class_url'],),))
        
        #Modifying homework
        else: ##modifying the homework
            mod_homework=form.save(commit=False)
            mod_homework.modified_by=self.request.user
            mod_homework.modified_on=datetime.today()
            mod_homework.deleted=False
            mod_homework.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('homework_view', args=(self.kwargs['class_url'],),))
            