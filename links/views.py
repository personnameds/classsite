from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import Link, Add_LinkForm
from classsite.views import URLMixin
from classlists.models import Klass
from homework.models import Hwk_Details
from django.shortcuts import get_object_or_404
from datetime import date

class LinkListView(URLMixin, ListView):
    template_name="links/link_list.html"
    context_object_name='link_list'    
    
    def get_queryset(self):
        klass=get_object_or_404(Klass,name=self.kwargs['class_url'])
        link_list=Link.objects.prefetch_related().filter(klass=klass).order_by('subject')
        return link_list

class LinkCreateView(URLMixin, CreateView):
	model=Link
	form_class=Add_LinkForm
	template_name='generic/generic_form.html'
	title='Link'
	named_url='link-create-view'
	
	def get_initial(self, **kwargs):
	    initial=super(LinkCreateView, self).get_initial()
	    initial['klass']=Klass.objects.filter(name=self.kwargs['class_url'])
	    return initial
	
	def get_context_data(self, **kwargs):
	    klass=Klass.objects.get(name=self.kwargs['class_url'])
	    context=super(LinkCreateView, self).get_context_data(**kwargs)
	    context['form'].fields['hwk_details'].queryset=Hwk_Details.objects.filter(klass=klass).exclude(due_date__date__lt=(date.today())).prefetch_related().order_by('due_date')
	    return context
	
	def form_valid(self, form):
	    new_link=form.save(commit=False)
	    if new_link.subject==None:
	        new_link.subject='Other'
	    if form.cleaned_data['hwk_details']:
	        new_link.homework=form.cleaned_data['hwk_details'].homework
	    new_link.save()
	    for k in form.cleaned_data['klass']:
	        new_link.klass.add(k)
	    
	    return HttpResponseRedirect(reverse('link-list-view', args=(self.kwargs['class_url'],)))

class LinkUpdateView(URLMixin, UpdateView):
    model=Link
    form_class=Add_LinkForm
    template_name="generic/generic_modify.html"
    title='Link'
    named_url='link-update-view'

    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(name=self.kwargs['class_url'])
        context=super(LinkUpdateView, self).get_context_data(**kwargs)
        context['form'].fields['hwk_details'].queryset=Hwk_Details.objects.filter(klass=klass).exclude(due_date__date__lt=(date.today())).prefetch_related().order_by('due_date')
        return context
    
    def get_initial(self, **kwargs):
	    initial=super(LinkUpdateView, self).get_initial()
	    
	    if self.object.homework:
	        homework=self.object.homework
	        klass=Klass.objects.get(name=self.kwargs['class_url'])
	        initial['hwk_details']=Hwk_Details.objects.get(homework=self.object.homework, klass=klass)
	    return initial
	
    def form_valid(self, form):
        
        if self.request.POST['mod/del']=='Delete':
            del_link=self.object
            for k in form.cleaned_data['klass']:
                del_link.klass.remove(k)
            if del_link.klass.count()==0:
                del_link.delete()
        
        else:
            mod_link=form.save(commit=False)
            if mod_link.subject==None:
                mod_link.subject='Other'
            if form.cleaned_data['hwk_details']:
                mod_link.homework=form.cleaned_data['hwk_details'].homework
            
            mod_link.klass.clear()
            for k in form.cleaned_data['klass']:
                mod_link.klass.add(k) 
            
            mod_link.save()
        
        return HttpResponseRedirect(reverse('link-list-view', args=(self.kwargs['class_url'],)))

