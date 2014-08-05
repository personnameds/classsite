from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from homework.models import Hwk_Details, Homework
from homework.forms import Homework_Form
from classlists.models import Klass, KKSA_Staff
from kalendar.models import Kalendar
from datetime import datetime, date, timedelta
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist


class HomeworkListView(ListView):
    template_name="homework/homework_list.html"
    context_object_name='hwk_details_list'
    
    def get_queryset(self):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        return Hwk_Details.objects.all().exclude(due_date__date__lt=(date.today())).filter(klass=klass).select_related('homework')
       
    def get_context_data(self, **kwargs):
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

    #Choose Klass field only available for teachers
    def get_form(self, form_class):
        form=super(HomeworkCreateView, self).get_form(form_class)
        if not self.request.user.has_perm('classlists.is_kksastaff'):
            form.fields.pop('klass')
        return form
    
    def get_initial(self, **kwargs):
        initial=super(HomeworkCreateView, self).get_initial()
        initial['klass']=Klass.objects.filter(klass_name=self.kwargs['class_url'])
        return initial

    def form_valid(self, form): #hwk_form, details_form):
        new_homework=form.save(commit=False)
        new_homework.entered_by=self.request.user
        new_homework.entered_on=datetime.today()
        new_homework.save()
        
        new_details=Hwk_Details()
        new_details.hwk=new_homework
        new_details.due_date=form.cleaned_data['due_date']
        new_details.deleted=False
        if self.request.user.has_perm('classlists.is_kksastaff'):
            #creating multiple copies of the same hwk details record, one for each class
            for k in form.cleaned_data['klass']:
                new_details.pk=None
                new_details.klass=k
                new_details.save()
        else:
            new_details.klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
            new_details.save()

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

    def get_initial(self, **kwargs):
        initial=super(HomeworkUpdateView, self).get_initial()
        klass_list=[]
        for h in self.object.hwk_details_set.all():
            klass_list.append(h.klass)
        initial['klass']=klass_list
        return initial


    def form_valid(self, form):
        
        #Delete homework
        if self.request.POST['mod/del']=='Delete':
            #Saves the homework to be deleted
            del_homework=form.save()
            
            #Gets all the details related to that homework
            del_details_list=Hwk_Details.objects.filter(hwk=del_homework)
            #If Teacher
            if self.request.user.has_perm('classlists.is_kksastaff'):
                #delete the details for the homework
                for k in form.cleaned_data['klass']:
                    del_details=del_details_list.filter(klass=k)
                    del_details.delete()
            
                ##if no details left then delete the homework too
                if del_homework.hwk_details_set.count()==0:
                    del_homework.delete()
                    
            #if not a teacher
            else:    
                del_details=del_details_list.get(klass=Klass.objects.get(klass_name=self.kwargs['class_url']))
                del_details.modified_by=self.request.user
                del_details.modified_on=datetime.today()
                del_details.deleted=True
                del_details.save()
                        
            return HttpResponseRedirect(reverse('homework_view', args=(self.kwargs['class_url'],),))
        
                
        #Modifying homework
        else: ##modifying the homework
            #Saves the modified homework
            mod_homework=form.save()
            
            #Gets all the details related to that homework
            mod_details_list=Hwk_Details.objects.filter(hwk=mod_homework)

            #If Teacher
            if self.request.user.has_perm('classlists.is_kksastaff'):
                for k in form.cleaned_data['klass']:
                    try:
                        mod_details=mod_details_list.get(klass=k)
                    except ObjectDoesNotExist:
                        mod_details=Hwk_Details()
                        mod_details.hwk=mod_homework
                        mod_details.klass=k
                    mod_details.due_date=form.cleaned_data['due_date']
                    mod_details.modified_by=self.request.user
                    mod_details.modified_on=datetime.today()
                    mod_details.deleted=False
                    mod_details.save()
            
            #if not a teacher
            else:
                mod_details=mod_details_list.get(klass=Klass.objects.get(klass_name=self.kwargs['class_url']))
                mod_details.due_date=form.cleaned_data['due_date']
                mod_details.modified_by=self.request.user
                mod_details.modified_on=datetime.today()
                mod_details.deleted=False
                mod_details.save()                
            
            return HttpResponseRedirect(reverse('homework_view', args=(self.kwargs['class_url'],),))
