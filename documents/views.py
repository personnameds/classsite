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
        return Document.objects.select_related().filter(klass=klass)
        
    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context=super(DocumentListView, self).get_context_data(**kwargs)
        context['klass']=klass
        context['path']=self.request.path
        
        document_list=Document.objects.select_related().filter(klass=klass)
        subjects=document_list.values_list('subject', flat=True).distinct()
        context['subject_list']=subjects
        return context


class DocumentCreateView(CreateView):
	model=Document
	form_class=Add_Document_Form
	template_name="documents/document_form.html"
	
# 	def get_initial(self, **kwargs):
# 	    initial=super(DocumentCreateView, self).get_initial()
# 	    class_url=self.kwargs['class_url']
# 	    class_db=Classes.objects.filter(classes=self.kwargs['class_url'])
# 	    initial['class_db']=class_db
# 	    return initial
	
	def get_context_data(self, **kwargs):
	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    context=super(DocumentCreateView, self).get_context_data(**kwargs)
	    context['form'].fields['homework'].queryset=Homework.objects.exclude(due_date__date__lt=(date.today())).filter(klass=klass)
	    context['klass']=klass
	    context['path']=self.request.path
	    return context
	    
	def form_valid(self, form):
	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    
	    new_document=form.save(commit=False)
	    if new_document.subject == None:
	        new_document.subject='Other'
	    new_document.filename=new_document.attached_file.name
	    new_document.save()
	    new_document.klass.add(klass)
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
        context['path']=self.request.path
        return context
        
    def form_valid(self, form):
        pk=self.kwargs['pk']
        new_document=Document.objects.get(id=pk)
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        if self.request.POST['mod/del']=='Delete':
            new_document.delete()
        else:
            new_document=form.save(commit=False)
            new_document.filename=(new_document.attached_file.name).lstrip('attachments/')
            new_document.save()
            new_document.klass.add(klass)
        return HttpResponseRedirect(reverse('document_view', args=(self.kwargs['class_url'],),))