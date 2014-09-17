from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from documents.models import Document
from documents.forms import Add_Document_Form
from classlists.models import Klass
from homework.models import Homework, Hwk_Details
from django.core.urlresolvers import reverse
from datetime import date, timedelta
from classpage.views import URLMixin
from django.shortcuts import get_object_or_404

class DocumentListView(URLMixin, ListView):
    template_name="documents/document_list.html"
    context_object_name="combo_list"
    
    def get_queryset(self):
        klass=get_object_or_404(Klass,klass_name=self.kwargs['class_url'])
        document_list=Document.objects.prefetch_related().filter(klass=klass).order_by('subject')
        combo_list=[]
        for d in document_list:
        	if d.homework:
        		combo_list.append((d,d.homework.hwk_details_set.get(klass=klass)))
        	else:
        		combo_list.append((d,None))
        return combo_list

class DocumentCreateView(CreateView):
	model=Document
	form_class=Add_Document_Form
	template_name="generic/generic_doc_form.html"
	title='Document'
	
	def get_initial(self, **kwargs):
	    initial=super(DocumentCreateView, self).get_initial()
	    initial['klass']=Klass.objects.filter(klass_name=self.kwargs['class_url'])
	    return initial

	def get_context_data(self, **kwargs):
	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    context=super(DocumentCreateView, self).get_context_data(**kwargs)
	    context['form'].fields['hwk_details'].queryset=Hwk_Details.objects.filter(klass=klass).exclude(due_date__date__lt=(date.today())).prefetch_related().order_by('due_date')
	    context['klass']=klass
	    context['next']=self.request.path
	    return context

	def form_valid(self, form):
	    new_document=form.save(commit=False)
	    new_document.filename=new_document.attached_file.name
	    if form.cleaned_data['hwk_details']:
	    	new_document.homework=form.cleaned_data['hwk_details'].hwk
	    new_document.save()
	    for k in form.cleaned_data['klass']:
	        new_document.klass.add(k)
	    
	    return HttpResponseRedirect(reverse('document_view', args=(self.kwargs['class_url'],),))

class DocumentUpdateView(UpdateView):
    model=Document
    form_class=Add_Document_Form
    template_name="generic/generic_modify_doc.html"
    title='Document'
    
    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context=super(DocumentUpdateView, self).get_context_data(**kwargs)
        context['form'].fields['hwk_details'].queryset=Hwk_Details.objects.filter(klass=klass)
        context['klass']=klass
        context['next']=self.request.path
        return context
    
    def get_intial(self, **kwargs):
        initial=super(DocumentUpdateView, self).get_initial()
        klass_list=[]
        for k in self.object.klass:
            klass_list.append(k)
        initial['klass']=klass_list
        
        if self.object.homework:
            homework=self.object.homework
            klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
            initial['hwk_details']=self.object.homework.hwk_details_set.filter(klass=klass)
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
                mod_doc.homework=form.cleaned_data['hwk_details'].hwk
            for k in form.cleaned_data['klass']:
                mod_doc.klass.add(k)
            
            mod_doc.save()
        return HttpResponseRedirect(reverse('document_view', args=(self.kwargs['class_url'],),))
