from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from homepage.models import Homepage, Homepage_Form
from classlists.models import Klass
from django import forms
from datetime import date

class HomepageListView(ListView):
    template_name='homepage/homepage_list.html'
    context_object_name='homepage_list'
    
    def get_queryset(self):
        return Homepage.objects.filter(klass__klass_name=self.kwargs['class_url']).order_by('-date')[:5]
        
    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(HomepageListView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=klass)
        context['next']=self.request.path
        return context


class HomepageCreateView(CreateView):
	model=Homepage
	template_name='homepage/homepage_form.html'
	    	
	def get_context_data(self, **kwargs):
	    klass=self.kwargs['class_url']
	    context=super(HomepageCreateView, self).get_context_data(**kwargs)
	    context['klass']=Klass.objects.get(klass_name=klass)
	    context['next']=self.request.path 
	    return context
    
	def form_valid(self, form):
		new_homepage=form.save(commit=False)
		new_homepage.date=date.today()
		new_homepage.klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
		new_homepage.entered_by=self.request.user
		new_homepage.save()
		return HttpResponseRedirect(reverse_lazy('homepage-list-view', args=(new_homepage.klass.klass_name,),))

class HomepageUpdateView(UpdateView):
    model=Homepage
    form_class=Homepage_Form
    template_name="homepage/modify_homepage.html"

    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(HomepageUpdateView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=klass)
        context['next']=self.request.path
        return context
        
    def get_form(self, form_class):
        form=super(HomepageUpdateView, self).get_form(form_class)
        form.fields['entered_by'].widget=forms.HiddenInput()
        form.fields['klass'].widget=forms.HiddenInput()
        form.fields['date'].widget=forms.HiddenInput()
        return form

    def get_form_kwargs(self):
        kwargs=super(HomepageUpdateView, self).get_form_kwargs()
        kwargs.update({'request':self.request})
        return kwargs
        
    def form_valid(self, form):
        pk=self.kwargs['pk']
        new_homepage=Homepage.objects.get(id=pk)
        if self.request.POST['mod/del']=='Delete':
            new_homepage.delete()
            return HttpResponseRedirect(reverse_lazy('homepage-list-view', args=(new_homepage.klass.klass_name,),))
        else:
            new_homepage=form.save()
            return HttpResponseRedirect(reverse_lazy('homepage-list-view', args=(new_homepage.klass.klass_name,),))
            

