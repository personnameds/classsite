from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Classpage
from django.shortcuts import get_object_or_404
from classlists.models import Klass
from datetime import date



class URLMixin(object):
	def get_klass(self):
		return get_object_or_404(Klass,name=self.kwargs['class_url'])
	
	def get_next(self):
		return self.request.path
	
	def get_context_data(self, **kwargs):
		ctx=super(URLMixin, self).get_context_data(**kwargs)
		ctx['klass']=self.get_klass()
		ctx['next']=self.get_next()
		return ctx

class ClasspageListView(URLMixin, ListView):
	template_name='classpage/classpage_list.html'
	context_object_name='classpage_list'

	def get_queryset(self):
	    return Classpage.objects.filter(klass__name=self.kwargs['class_url']).order_by('-date')[:5]

class ClasspageCreateView(URLMixin, CreateView):
	model=Classpage
	template_name='generic/generic_form.html'
	fields=['message','klass']

	def form_valid(self, form):
	    new_schoolpage=form.save(commit=False)
	    new_schoolpage.date=date.today()
	    new_schoolpage.entered_by=self.request.user
	    new_schoolpage.save()
	    return HttpResponseRedirect(reverse('classpage-list-view'))




# class ClasspageCreateView(URLMixin, CreateView):
#     form_class=Classpage_Form
#     model=Classpage
#     template_name='generic/generic_form.html'
#     title='Class Message'
#     
#     def get_initial(self, **kwargs):
#         initial=super(ClasspageCreateView, self).get_initial()
#         initial['klass']=Klass.objects.filter(klass_name=self.kwargs['class_url'])
#         return initial
#         
#     def form_valid(self, form):
#         new_classpage=form.save(commit=False)
#         new_classpage.date=date.today()
#         new_classpage.entered_by=self.request.user
#         
#         for k in form.cleaned_data['klass']:
#             new_classpage.pk=None
#             new_classpage.klass=k
#             new_classpage.save()
# 
#         return HttpResponseRedirect(reverse('classpage-list-view', args=(self.kwargs['class_url'],),))