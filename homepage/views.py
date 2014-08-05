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
    form_class=Homepage_Form
    model=Homepage
    template_name='homepage/homepage_form.html'
    
    def get_context_data(self, **kwargs):
        klass=self.kwargs['class_url']
        context=super(HomepageCreateView, self).get_context_data(**kwargs)
        context['klass']=Klass.objects.get(klass_name=klass)
        context['next']=self.request.path
        return context
    
    def get_initial(self, **kwargs):
        initial=super(HomepageCreateView, self).get_initial()
        initial['klass']=Klass.objects.filter(klass_name=self.kwargs['class_url'])
        return initial
        
    def form_valid(self, form):
        new_homepage=form.save(commit=False)
        new_homepage.date=date.today()
        new_homepage.entered_by=self.request.user
        
        for k in form.cleaned_data['klass']:
            new_homepage.pk=None
            new_homepage.klass=k
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
        form.fields.pop('klass')
        return form

    def form_valid(self, form):
        new_homepage=form.save(commit=False)
        if self.request.POST['mod/del']=='Delete':
            new_homepage.delete()
        else:
            new_homepage.entered_by=self.request.user
            new_homepage.save()
        return HttpResponseRedirect(reverse_lazy('homepage-list-view', args=(new_homepage.klass.klass_name,),))
            