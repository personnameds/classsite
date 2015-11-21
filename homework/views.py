from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from classsite.views import URLMixin
from .models import Homework, Hwk_Details
from .forms import Homework_Form
from classlists.models import Klass
from django.shortcuts import get_object_or_404
from datetime import date
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class HomeworkListView(URLMixin, ListView):
    template_name="homework/homework_list.html"
    context_object_name='homework_list'
    model=Homework
    
    def get_queryset(self):
        klass=get_object_or_404(Klass,name=self.kwargs['class_url'])
        
        homework_list=[]
        homework_objects=Homework.objects.filter(hwk_details__klass=klass).exclude(hwk_details__due_date__date__lt=(date.today())).prefetch_related().order_by('hwk_details__due_date')
        
        for homework in homework_objects:
            homework_list.append((
                homework, 
                homework.hwk_details_set.filter(klass=klass), 
                homework.document_set.filter(klass=klass), 
                homework.link_set.filter(klass=klass),
                ))
        return homework_list

class HomeworkCreateView(URLMixin, CreateView):
    model=Homework
    form_class=Homework_Form
    title='Homework'
    template_name='generic/generic_form.html'
    named_url='homework-create-view'
    
    def get_form(self, form_class):
        form=super(HomeworkCreateView, self).get_form(form_class)
        if not self.request.user.has_perm('homework.can_add_multi_classes'):
            form.fields.pop('klass')
        return form
    
    def get_initial(self, **kwargs):
        initial=super(HomeworkCreateView, self).get_initial()
        initial['klass']=Klass.objects.filter(name=self.kwargs['class_url'])
        return initial
   
    def form_valid(self, form):
        new_homework=form.save(commit=False)
        new_homework.entered_by=self.request.user
        new_homework.entered_on=date.today()
        new_homework.save()
        
        if self.request.user.has_perm('homework.can_add_multi_classes'):
            klass_list=form.cleaned_data['klass']
        else:
            klass_list=Klass.objects.filter(name=self.kwargs['class_url'])
            
        for klass in klass_list:
            new_detail=Hwk_Details(
                            homework=new_homework,
                            due_date=form.cleaned_data['due_date'],
                            klass=klass,
                            deleted=False,
                            )
            new_detail.save()
        return HttpResponseRedirect(reverse('homework-list-view', args=(self.kwargs['class_url'],)))


class HomeworkUpdateView(URLMixin, UpdateView):
    model=Homework
    form_class=Homework_Form
    title='Homework'
    template_name='generic/generic_modify.html'
    named_url='homework-update-view'
    
    def get_form(self, form_class):
        form=super(HomeworkUpdateView, self).get_form(form_class)
        if not self.request.user.has_perm('homework.can_add_multi_classes'):
            form.fields.pop('klass')
        return form

    def get_initial(self, **kwargs):
        initial=super(HomeworkUpdateView, self).get_initial()
        klass=Klass.objects.get(name=self.kwargs['class_url'])
        homework=Homework.objects.get(pk=self.object.pk)
        hwk_details=homework.hwk_details_set.all()
        klass_list=[]
        for detail in hwk_details:
            klass_list.append(detail.klass)
        initial['klass']=klass_list
        
        detail=homework.hwk_details_set.get(klass=klass)
        initial['due_date']=detail.due_date
        return initial
        
    def form_valid(self, form):
    
        if self.request.POST['mod/del']=='Delete':
            del_homework=self.object
            if self.request.user.has_perm('homework.can_add_multi_classes'):
                klass_list=form.cleaned_data['klass']
                for klass in klass_list:
                    del_homework.hwk_details_set.filter(klass=klass).delete()
                    del_homework.document_set.filter(klass=klass).delete()
                if del_homework.hwk_details_set.count()==0:
                    del_homework.delete()   
            else:
                klass=Klass.objects.filter(name=self.kwargs['class_url'])
                del_detail=del_homework.hwk_details_set.get(klass=klass)
                del_detail.modified_by=self.request.user
                del_detail.modified_on=date.today()
                del_detail.deleted=True
                del_detail.save()
        else:
            new_homework=form.save(commit=False)
            new_homework.save()
        
            if self.request.user.has_perm('homework.can_add_multi_classes'):
                klass_list=form.cleaned_data['klass']
            else:
                klass_list=Klass.objects.filter(name=self.kwargs['class_url'])
            
            for klass in klass_list:
                if new_homework.hwk_details_set.filter(klass=klass):
                    new_detail=new_homework.hwk_details_set.get(klass=klass)
                    new_detail.due_date=form.cleaned_data['due_date']
                    new_detail.modified_by=self.request.user
                    new_detail.modified_on=date.today()
                    new_detail.deleted=False
                    new_detail.save()
                else:
                    new_detail=Hwk_Details(
                                    homework=new_homework,
                                    due_date=form.cleaned_data['due_date'],
                                    klass=klass,
                                    deleted=False,
                                    modified_by=self.request.user,
                                    modified_on=date.today(),
                                    )
                    new_detail.save()
                    
        return HttpResponseRedirect(reverse('homework-list-view', args=(self.kwargs['class_url'],)))
        
