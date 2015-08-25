from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Schoolpage

class SchoolpageListView(ListView):
	template_name='schoolpage/index.html'
	context_object_name='schoolpage_list'
	a=z
	
	def get_queryset(self):
		return Schoolpage.objects.all().order_by('-date')[:5]

# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse_lazy
# from django.views.generic import ListView
# from django.views.generic.edit import CreateView, UpdateView
# from schoolpage.models import Schoolpage, Schoolpage_Form
# from classlists.models import Klass
# from django import forms
# from datetime import date
# 
# class SchoolpageListView(ListView):
#     template_name='schoolpage/index.html'
#     context_object_name='schoolpage_list'
#     
#     def get_queryset(self):
#         return Schoolpage.objects.all().order_by('-date')[:5]
#     
#     def get_context_data(self, **kwargs):
# 	    klass_list=Klass.objects.all().order_by('klass_name')
# 	    context=super(SchoolpageListView, self).get_context_data(**kwargs)
# 	    context['klass_list']=klass_list
# 	    context['next']=self.request.path
# 	    return context