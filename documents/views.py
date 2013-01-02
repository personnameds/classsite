from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from documents.models import Document, Add_Document_Form
from classlists.models import Classes
from homework.models import Homework
from django.core.urlresolvers import reverse_lazy

from datetime import date, timedelta

class DocumentListView(ListView):
    template_name="document_list.html"
    
    def get_queryset(self):
        class_db=Classes.objects.get(classes=self.kwargs['class_url'])
        return Document.objects.select_related().filter(class_db__exact=class_db)
        
    def get_context_data(self, **kwargs):
        class_url=self.kwargs['class_url']
        context=super(DocumentListView, self).get_context_data(**kwargs)
        context['class_url']=class_url.lower()
        class_db=Classes.objects.get(classes=self.kwargs['class_url'])
        document_list=Document.objects.select_related().filter(class_db__exact=class_db)
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
	    class_url=self.kwargs['class_url']
	    class_db=Classes.objects.get(classes=self.kwargs['class_url'])
	    context=super(DocumentCreateView, self).get_context_data(**kwargs)
	    context['form'].fields['homework'].queryset=Homework.objects.exclude(due_date__date__lt=(date.today())).filter(class_db=class_db)
	    context['class_url']=class_url.lower()
	    return context
	    
	def form_valid(self, form):
	    class_db=Classes.objects.get(classes=self.kwargs['class_url'])
	    
	    new_document=form.save(commit=False)
	    if new_document.subject == None:
	        new_document.subject='Other'
	    new_document.filename=new_document.attached_file.name
	    new_document.save()
	    new_document.class_db.add(class_db)
	    return HttpResponseRedirect(reverse_lazy('document-list-view', args=(self.kwargs['class_url'],),))

class DocumentUpdateView(UpdateView):
    model=Document
    form_class=Add_Document_Form
    template_name="documents/modify_document.html"

    def get_context_data(self, **kwargs):
        class_url=self.kwargs['class_url']
        context=super(DocumentUpdateView, self).get_context_data(**kwargs)
        context['class_url']=class_url.lower()
        return context
        
    def form_valid(self, form):
        pk=self.kwargs['pk']
        new_document=Document.objects.get(id=pk)
        class_db=Classes.objects.get(classes=self.kwargs['class_url'])
        if self.request.POST['mod/del']=='Delete':
            new_document.delete()
            return HttpResponseRedirect(reverse_lazy('document-list-view', args=(self.kwargs['class_url'],),))
        else:
            new_document=form.save(commit=False)
            new_document.filename=(new_document.attached_file.name).lstrip('attachments/')
            new_document.save()
            new_document.class_db.add(class_db)
            return HttpResponseRedirect(reverse_lazy('document-list-view', args=(self.kwargs['class_url'],),))