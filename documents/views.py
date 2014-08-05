from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from documents.models import Document, Add_Document_Form
from classlists.models import Klass
from homework.models import Homework
from django.core.urlresolvers import reverse
from datetime import date, timedelta

class DocumentListView(ListView):
    template_name="document_list.html"
    
    def get_queryset(self):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        return Document.objects.filter(klass=klass)
        
    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context=super(DocumentListView, self).get_context_data(**kwargs)
        context['klass']=klass
        context['next']=self.request.path
        
        document_list=Document.objects.filter(klass=klass)
        subjects=document_list.values_list('subject', flat=True).distinct()
        context['subject_list']=subjects
        return context


class DocumentCreateView(CreateView):
	model=Document
	form_class=Add_Document_Form
	template_name="documents/document_form.html"
	
	def get_initial(self, **kwargs):
	    initial=super(DocumentCreateView, self).get_initial()
	    initial['klass']=Klass.objects.filter(klass_name=self.kwargs['class_url'])
	    return initial

	def get_context_data(self, **kwargs):
	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    context=super(DocumentCreateView, self).get_context_data(**kwargs)
	    context['form'].fields['homework'].queryset=Homework.objects.exclude(due_date__date__lt=(date.today())).filter(klass=klass)
	    context['klass']=klass
	    context['next']=self.request.path
	    return context

	def form_valid(self, form):
	    new_document=form.save(commit=False)
	    new_document.filename=new_document.attached_file.name
	    new_document.save()
	    for k in form.cleaned_data['klass']:
	        new_document.klass.add(k)
 	    return HttpResponseRedirect(reverse('document_view', args=(self.kwargs['class_url'],),))

class DocumentUpdateView(UpdateView):
    model=Document
    form_class=Add_Document_Form
    template_name="documents/modify_document.html"

    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context=super(DocumentUpdateView, self).get_context_data(**kwargs)
        context['form'].fields['homework'].queryset=Homework.objects.exclude(due_date__date__lt=(date.today())).filter(klass=klass)
        context['klass']=klass
        context['next']=self.request.path
        return context
    
    def form_valid(self, form):

        if self.request.POST['mod/del']=='Delete':
            del_document=form.save(commit=False)
            for k in form.cleaned_data['klass']:
                del_document.klass.remove(k)
            if del_document.klass.count()==0:
                del_document.delete()
        else:
            mod_document=form.save(commit=False)
            a=mod_document.attached_file
            mod_document.save()
            mod_document.klass.clear()
            for k in form.cleaned_data['klass']:
                mod_document.klass.add(k)
        return HttpResponseRedirect(reverse('document_view', args=(self.kwargs['class_url'],),))
        
