# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
# from django.views.generic.edit import CreateView, UpdateView
# from homepage.models import Homepage, Homepage_Form
from classlists.models import Klass
#from django.shortcuts import get_object_or_404
# from django import forms
# 
# from datetime import date
# 
class HomepageListView(ListView):
    template_name='test.html' #"homepage_list.html"
    template_object_name='classes' #django appends _list to this in template
    model=Klass
    
#     def get_queryset(self):
#         class_db=get_object_or_404(Classes, classes=self.kwargs['class_url'])
#         return Homepage.objects.filter(class_db=class_db)[:5]
        
    def get_context_data(self, **kwargs):
        class_url=self.kwargs['class_url']
        context=super(HomepageListView, self).get_context_data(**kwargs)
        context['class_url']=class_url.lower()
        return context



# class HomepageCreateView(CreateView):
# 	model=Homepage
# 	form_class=Homepage_Form
# 	template_name="homepage_form.html"
# 	    	
# 	def get_context_data(self, **kwargs):
# 	    class_url=self.kwargs['class_url']
# 	    context=super(HomepageCreateView, self).get_context_data(**kwargs)
# 	    context['class_url']=class_url.lower()
# 	    return context
# 	
# 	def form_valid(self, form):
# 		new_homepage=form.save(commit=False)
# 		new_homepage.date=date.today()
# 		new_homepage.class_db=Classes.objects.get(classes=self.kwargs['class_url'])
# 		new_homepage.entered_by=self.request.user
# 		new_homepage.save()
# 		return HttpResponseRedirect('/'+self.kwargs['class_url'])
# 	
# 	def get_form_kwargs(self):
# 	    kwargs=super(HomepageCreateView, self).get_form_kwargs()
# 	    kwargs.update({'request':self.request},)
# 	    return kwargs
# 
# class HomepageUpdateView(UpdateView):
#     model=Homepage
#     form_class=Homepage_Form
#     template_name="homepage/modify_homepage.html"
# 
#     def get_context_data(self, **kwargs):
#         class_url=self.kwargs['class_url']
#         context=super(HomepageUpdateView, self).get_context_data(**kwargs)
#         context['class_url']=class_url.lower()
#         return context
#         
#     def get_form(self, form_class):
#         form=super(HomepageUpdateView, self).get_form(form_class)
#         form.fields['entered_by'].widget=forms.HiddenInput()
#         form.fields['class_db'].widget=forms.HiddenInput()
#         form.fields['date'].widget=forms.HiddenInput()
#         return form
# 
#     def get_form_kwargs(self):
#         kwargs=super(HomepageUpdateView, self).get_form_kwargs()
#         kwargs.update({'request':self.request})
#         return kwargs
#         
#     def form_valid(self, form):
#         pk=self.kwargs['pk']
#         new_homepage=Homepage.objects.get(id=pk)
#         if self.request.POST['mod/del']=='Delete':
#             new_homepage.delete()
#             return HttpResponseRedirect(reverse_lazy('homepage-list-view', args=(self.kwargs['class_url'],),))
#         else:
#             new_homepage=form.save()
#             return HttpResponseRedirect(reverse_lazy('homepage-list-view', args=(self.kwargs['class_url'],),))
#             

