from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from schoolpage.models import Schoolpage, Schoolpage_Form
from classlists.models import Klass
from django import forms
from datetime import date

class SchoolpageListView(ListView):
    template_name='schoolpage/index.html'
    context_object_name='schoolpage_list'
    
    def get_queryset(self):
        return Schoolpage.objects.all().order_by('-date')[:5]
    
    def get_context_data(self, **kwargs):
	    klass_list=Klass.objects.all().order_by('klass_name')
	    context=super(SchoolpageListView, self).get_context_data(**kwargs)
	    context['klass_list']=klass_list
	    context['next']=self.request.path
	    return context

class SchoolpageCreateView(CreateView):
	model=Schoolpage
	template_name='schoolpage/schoolpage_form.html'
	    	
	def get_context_data(self, **kwargs):
	    context=super(SchoolpageCreateView, self).get_context_data(**kwargs)
	    context['next']=self.request.path 
	    return context
	
	def form_valid(self, form):
		new_schoolpage=form.save(commit=False)
		new_schoolpage.date=date.today()
		new_schoolpage.entered_by=self.request.user
		new_schoolpage.save()
		return HttpResponseRedirect(reverse_lazy('schoolpage-list-view'))

class SchoolpageUpdateView(UpdateView):
    model=Schoolpage
    form_class=Schoolpage_Form
    template_name="schoolpage/modify_schoolpage.html"

    def get_context_data(self, **kwargs):
        context=super(SchoolpageUpdateView, self).get_context_data(**kwargs)
        context['next']=self.request.path
        return context
        
    def get_form(self, form_class):
        form=super(SchoolpageUpdateView, self).get_form(form_class)
        form.fields['entered_by'].widget=forms.HiddenInput()
        form.fields['date'].widget=forms.HiddenInput()
        return form

    def get_form_kwargs(self):
        kwargs=super(SchoolpageUpdateView, self).get_form_kwargs()
        kwargs.update({'request':self.request})
        return kwargs
        
    def form_valid(self, form):
        pk=self.kwargs['pk']
        new_schoolpage=Schoolpage.objects.get(id=pk)
        if self.request.POST['mod/del']=='Delete':
            new_schoolpage.delete()
            return HttpResponseRedirect(reverse_lazy('schoolpage-list-view'))
        else:
            new_schoolpage=form.save()
            return HttpResponseRedirect(reverse_lazy('schoolpage-list-view'))
            

