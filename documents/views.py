from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import Document, Add_DocumentForm
from classsite.views import URLMixin
from django.shortcuts import get_object_or_404
from classlists.models import Klass
from homework.models import Homework, Hwk_Details
from datetime import date

class DocumentListView(URLMixin, ListView):
    template_name="documents/document_list.html"
    context_object_name="document_list"
    
    def get_queryset(self):
        klass=get_object_or_404(Klass,name=self.kwargs['class_url'])
        document_list=Document.objects.prefetch_related().filter(klass=klass).order_by('subject')
        return document_list
        
class DocumentCreateView(URLMixin, CreateView):
    model=Document
    form_class=Add_DocumentForm
    template_name="documents/doc_form.html"
    title='Document'
    
    def get_initial(self, **kwargs):
        initial=super(DocumentCreateView, self).get_initial()
        initial['klass']=Klass.objects.filter(name=self.kwargs['class_url'])
        return initial
    
    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(name=self.kwargs['class_url'])
        context=super(DocumentCreateView, self).get_context_data(**kwargs)
        context['form'].fields['hwk_details'].queryset=Hwk_Details.objects.filter(klass=klass).exclude(due_date__date__lt=(date.today())).prefetch_related().order_by('due_date')
        return context
    
    def form_valid(self, form):
        new_document=form.save(commit=False)
        new_document.filename=new_document.attached_file.name
        if form.cleaned_data['hwk_details']:
            new_document.homework=form.cleaned_data['hwk_details'].homework
        new_document.save()
        for k in form.cleaned_data['klass']:
            new_document.klass.add(k)
            
        return HttpResponseRedirect(reverse('document-list-view', args=(self.kwargs['class_url'],)))

class DocumentUpdateView(URLMixin, UpdateView):
    model=Document
    form_class=Add_DocumentForm
    template_name="documents/modify_doc.html"
    title='Document'
    
    def get_initial(self, **kwargs):
        initial=super(DocumentUpdateView, self).get_initial()

        if self.object.homework:
            homework=self.object.homework
            klass=Klass.objects.get(name=self.kwargs['class_url'])
            initial['hwk_details']=Hwk_Details.objects.get(homework=self.object.homework, klass=klass)
        return initial

    
    def form_valid(self, form):
        if self.request.POST['mod/del']=='Delete':
            del_doc=self.object
            
            for k in form.cleaned_data['klass']:
                del_doc.klass.remove(k)
            if del_doc.klass.count()==0:
                del_doc.delete()
        
        else:
            mod_doc=form.save(commit=False)
            if form.cleaned_data['hwk_details']:
                mod_doc.homework=form.cleaned_data['hwk_details'].homework
            
            mod_doc.klass.clear()
            for k in form.cleaned_data['klass']:
                mod_doc.klass.add(k)
            
            mod_doc.save()
        return HttpResponseRedirect(reverse('document-list-view', args=(self.kwargs['class_url'],)))
