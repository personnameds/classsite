from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from homework.models import Hwk_Details, Homework
from links.models import Link
from documents.models import Document
from homework.forms import Hwk_Details_Form, Hwk_Details_Staff_Form
from classlists.models import Klass, KKSA_Staff
from kalendar.models import Kalendar
from datetime import datetime, date, timedelta
from django.core.urlresolvers import reverse


class HomeworkListView(ListView):
    template_name="homework/homework_list.html"
    context_object_name='combo_list'
    
    def get_queryset(self):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        
        details_list=Hwk_Details.objects.filter(klass=klass).exclude(due_date__date__lt=(date.today())).prefetch_related()
        combo_list=[]
        for d in details_list:
            h=d.hwk
            l=h.link_set.filter(klass=klass)
            combo_list.append((h,d,l))
        return combo_list

    def get_context_data(self, **kwargs):
        context=super(HomeworkListView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['next']=self.request.path
        context['now']=datetime.now()
        return context

class HomeworkCreateView(CreateView):
    model=Homework
    
    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(HomeworkCreateView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['next']=self.request.path
        context['title']='Homework'
        return context

	def get_form_class(self):
		if self.request.user.has_perm('classlists.is_kksastaff'):
			return Hwk_Details_Staff_Form
		return Hwk_Details_Form

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

	def get_template_names(self):
		if self.request.user.has_perm('classlists.is_kksastaff'):
			return "homework/homework_form.html"
		return "generic/generic_form.html"

    def form_valid(self, form):
        new_homework=Homework(
                        entered_by=self.request.user,
                        entered_on=datetime.today(),
                        )
        new_homework.save()
        
        new_details=form.save(commit=False)
        new_details.deleted=False
        new_details.hwk=new_homework

        if self.request.user.has_perm('classlists.is_kksastaff'):
            #creating multiple copies of the same hwk details record, one for each class
            for k in form.cleaned_data['klass']:
                new_details.pk=None
                new_details.klass=k
                new_details.save()
        	
        	if form.cleaned_data['link']:
        		new_link=Link(
        					link=form.cleaned_data['link'],
        					description=form.cleaned_data['link_description'],
        					homework=new_homework,
        					subject=new_details.subject,
        					)
        		new_link.save()
        		for k in form.cleaned_data['klass']:
        			new_link.klass.add(k)

        	a=z
        	if form.cleaned_data['attached_file']:
        	    a=z
        	    new_document=Document(
        			attached_file=cleaned_data['attached_file'],
        			filename=attached_file.name
        			description=form.cleaned_data['document_description'],
        			homework=new_homework,
        			subject=new_details.subject,
        			)
        		new_document.save()
        		for k in form.cleaned_data['klass']:
        		    new_document.klass.add(k)
        	
        else:
            new_details.klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
            new_details.save()
        
        return HttpResponseRedirect(reverse('homework_view', args=(self.kwargs['class_url'],),))

class HomeworkUpdateView(UpdateView):
    model=Hwk_Details
    form_class=Hwk_Details_Form
    template_name="generic/generic_modify.html"

    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context=super(HomeworkUpdateView, self).get_context_data(**kwargs)
        context['klass']=klass
        context['next']=self.request.path
        context['title']='Homework'
        return context

    #Choose Klass field only available for teachers
    def get_form(self, form_class):
        form=super(HomeworkUpdateView, self).get_form(form_class)
        if not self.request.user.has_perm('classlists.is_kksastaff'):
            form.fields.pop('klass')
        return form
    
    def get_initial(self, **kwargs):
        initial=super(HomeworkUpdateView, self).get_initial()
        #gets the homework object for the single detail
        homework=self.object.hwk
        klass_list=[]
        #loops through all the details for that homework to get all the classes
        for d in homework.hwk_details_set.all():
            klass_list.append(d.klass)
        initial['klass']=klass_list
        return initial

    def form_valid(self, form):
        
        #Delete homework
        if self.request.POST['mod/del']=='Delete':
            
            del_detail=self.object
            del_homework=self.object.hwk
            del_details_list=del_homework.hwk_details_set.all()
            #If Teacher
            if self.request.user.has_perm('classlists.is_kksastaff'):
                #delete the details for the homework
                for k in form.cleaned_data['klass']:
                    del_details_list.filter(klass=k).delete()
                ##if no details left then delete the homework too
                if del_homework.hwk_details_set.count()==0:
                    del_homework.delete()
                    
            #if not a teacher
            else:
                del_detail.modified_by=self.request.user
                del_detail.modified_on=datetime.today()
                del_detail.deleted=True
                del_detail.save()
                        
            return HttpResponseRedirect(reverse('homework_view', args=(self.kwargs['class_url'],),))
        
                
        #Modifying homework
        else: ##modifying the homework


            mod_homework=self.object.hwk
            mod_details_list=mod_homework.hwk_details_set.all()
            
            mod_detail=form.save(commit=False)   
            mod_detail.modified_by=self.request.user
            mod_detail.modified_on=datetime.today()
            mod_detail.deleted=False
            #If Teacher
            if self.request.user.has_perm('classlists.is_kksastaff'):
                for k in form.cleaned_data['klass']:
                    #if modify detail doesn't exist then create it
                    if not mod_details_list.filter(klass=k):
                         mod_detail.pk=None
                         mod_detail.hwk=mod_homework
                    else:
                        mod_detail.pk=mod_details_list.get(klass=k).pk
                        
                    mod_detail.klass=k
                    mod_detail.save()
            #if not a teacher
            else:
                mod_detail.klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
                mod_detail.modified_by=self.request.user
                mod_detail.modified_on=datetime.today()
                mod_detail.deleted=False
                mod_detail.save()                
            
            return HttpResponseRedirect(reverse('homework_view', args=(self.kwargs['class_url'],),))
