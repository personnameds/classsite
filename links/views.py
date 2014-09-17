from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from links.models import Link 
from links.forms import Add_Link_Form
from classlists.models import Klass
from homework.models import Hwk_Details
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from datetime import date, timedelta

class LinkListView(ListView):
    template_name="links/link_list.html"
    context_object_name='combo_list'    
    
    def get_queryset(self):
        klass=get_object_or_404(Klass,klass_name=self.kwargs['class_url'])
        links_list=Link.objects.prefetch_related().filter(klass=klass).order_by('subject')
        combo_list=[]
        for l in links_list:
            if l.homework:
                combo_list.append((l,l.homework.hwk_details_set.get(klass=klass)))
            else:
                combo_list.append((l,None))
        return combo_list

    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context=super(LinkListView, self).get_context_data(**kwargs)
        context['klass']=klass
        context['next']=self.request.path
        return context



class LinkCreateView(CreateView):
	model=Link
	form_class=Add_Link_Form
	template_name='generic/generic_form.html'
	
	def get_initial(self, **kwargs):
	    initial=super(LinkCreateView, self).get_initial()
	    initial['klass']=Klass.objects.filter(klass_name=self.kwargs['class_url'])
	    return initial

	def get_context_data(self, **kwargs):
	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    context=super(LinkCreateView, self).get_context_data(**kwargs)
	    context['form'].fields['hwk_details'].queryset=Hwk_Details.objects.filter(klass=klass).exclude(due_date__date__lt=(date.today())).prefetch_related().order_by('due_date')
	    context['klass']=klass
	    context['next']=self.request.path
	    context['title']='Link'
	    return context

  	def form_valid(self, form):
  	    new_link=form.save(commit=False)
  	    if new_link.subject==None:
  	        new_link.subject='Other'
  	    if form.cleaned_data['hwk_details']:
  	        new_link.homework=form.cleaned_data['hwk_details'].hwk
  	    new_link.save()
  	    for k in form.cleaned_data['klass']:
  	        new_link.klass.add(k)
  	        
  	    return HttpResponseRedirect(reverse('link_view', args=(self.kwargs['class_url'],),))


class LinkUpdateView(UpdateView):
    model=Link
    form_class=Add_Link_Form
    template_name="generic/generic_modify.html"

    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context=super(LinkUpdateView, self).get_context_data(**kwargs)
        context['form'].fields['hwk_details'].queryset=Hwk_Details.objects.filter(klass=klass)
        context['klass']=klass
        context['next']=self.request.path
        context['title']='Links'
        return context
    
    def get_initial(self, **kwargs):
	    initial=super(LinkUpdateView, self).get_initial()
	    klass_list=[]
	    a=self.object.klass
	    for k in self.object.klass.all():
	        klass_list.append(k)
	    initial['klass']=klass_list 
	    
	    if self.object.homework:
	        homework=self.object.homework
	        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	        initial['hwk_details']=self.object.homework.hwk_details_set.filter(klass=klass)
	    
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
                mod_link.homework=form.cleaned_data['hwk_details'].hwk
            for k in form.cleaned_data['klass']:
                mod_link.klass.add(k) 
                mod_link.save()
        
        return HttpResponseRedirect(reverse('link_view', args=(self.kwargs['class_url'],),))

