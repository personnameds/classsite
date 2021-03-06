from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import Schoolpage
from classlists.models import Klass
from django.core.urlresolvers import reverse
from datetime import date
from django.http import HttpResponseRedirect
from django.conf import settings
from classsite.views import SchoolNameMixin

class SchoolpageListView(SchoolNameMixin, ListView):
	template_name='schoolpage/index.html'
	context_object_name='schoolpage_list'
	
	def get_queryset(self):
	    return Schoolpage.objects.all().order_by('-date')[:5]
	
	def get_context_data(self, **kwargs):
	    klass_list=Klass.objects.all().order_by('name')
	    context=super(SchoolpageListView, self).get_context_data(**kwargs)
	    context['klass_list']=klass_list
	    return context

class SchoolpageCreateView(SchoolNameMixin, CreateView):
	model=Schoolpage
	template_name='schoolpage/add_schoolpage.html'
	fields=['message','image']

	def get_context_data(self, **kwargs):
	    klass_list=Klass.objects.all().order_by('name')
	    context=super(SchoolpageCreateView, self).get_context_data(**kwargs)
	    context['klass_list']=klass_list
	    return context

	def form_valid(self, form):
	    new_schoolpage=form.save(commit=False)
	    new_schoolpage.date=date.today()
	    new_schoolpage.entered_by=self.request.user
	    new_schoolpage.save()
	    return HttpResponseRedirect(reverse('schoolpage-list-view'))


class SchoolpageUpdateView(SchoolNameMixin, UpdateView):
    model=Schoolpage
    template_name="schoolpage/modify_schoolpage.html"
    fields=['message','image']
    
    def get_context_data(self, **kwargs):
	    klass_list=Klass.objects.all().order_by('name')
	    context=super(SchoolpageUpdateView, self).get_context_data(**kwargs)
	    context['klass_list']=klass_list
	    return context

    def form_valid(self, form):
        new_schoolpage=form.save(commit=False)
        if self.request.POST['mod/del']=='Delete':
            new_schoolpage.delete()
            return HttpResponseRedirect(reverse('schoolpage-list-view'))
        else:
            new_schoolpage.date=date.today()
            new_schoolpage.entered_by=self.request.user
            new_schoolpage.save()
            return HttpResponseRedirect(reverse('schoolpage-list-view'))
            
