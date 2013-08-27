from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from homework.models import Homework, Homework_Form
from classlists.models import Klass
from kalendar.models import Kalendar
from datetime import datetime, date, timedelta
from django.core.urlresolvers import reverse


class HomeworkListView(ListView):
    template_name="homework_list.html"
    
    def get_queryset(self):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        return Homework.objects.select_related().exclude(due_date__date__lte=(date.today())).filter(klass=klass)
        
    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(HomeworkListView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['path']=self.request.path
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
        context['path']=self.request.path
        return context
    
    def get_initial(self, **kwargs):
        initial=super(HomeworkCreateView, self).get_initial()
        
        klass=self.kwargs['class_url']
        klass=Klass.objects.filter(klass_name=self.kwargs['class_url'])
        
        initial['klass']=klass
        return initial

    def get_form_kwargs(self):
        kwargs=super(HomeworkCreateView, self).get_form_kwargs()
        kwargs.update({'request':self.request, 'klass':self.kwargs['class_url']})
        return kwargs

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
    
    def get_initial(self, **kwargs):
        initial=super(HomeworkUpdateView, self).get_initial()
    
        pk=self.kwargs['pk']
        h=Homework.objects.get(id=pk)
        initial['due_date']=h.due_date.date
        
        return initial

    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']    
        pk=self.kwargs['pk']
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        
        context=super(HomeworkUpdateView, self).get_context_data(**kwargs)
        context['klass']=klass
        return context

    def get_form_kwargs(self):
        kwargs=super(HomeworkUpdateView, self).get_form_kwargs()
        kwargs.update({'request':self.request, 'klass':self.kwargs['class_url']})
        return kwargs

    def form_valid(self, form):
        pk=self.kwargs['pk']
        h=Homework.objects.get(id=pk)
        klass=self.kwargs['class_url']
        if self.request.POST['mod/del']=='Delete':
            if self.request.user.is_staff:
                h.delete()
            else:
                del_homework=form.save(commit=False)
                del_homework.modified_by=self.request.user
                del_homework.modified_on=datetime.today()
                del_homework.deleted=True
                del_homework.save()
            return HttpResponseRedirect(reverse('homework_view', args=(self.kwargs['class_url'],),))
        else:
            mod_homework=form.save(commit=False)
            mod_homework.modified_by=self.request.user
            mod_homework.modified_on=datetime.today()
            mod_homework.deleted=False
            mod_homework.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('homework_view', args=(self.kwargs['class_url'],),))
            