from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import Classpage, Classpage_AddForm, Classpage_ModifyForm
from django.shortcuts import get_object_or_404
from classlists.models import Klass
from datetime import date
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

### Want to reverse or resolve the namedurl for the classbased view to use in action form
### so named url in action of form
### also used named url when you hit the cancel button
### can't I also used the named url for next????
### couldn't I also use the class_url as an argument so I do not need the context data and urlmixin??
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
	form_class=Classpage_AddForm
	template_name='generic/generic_form.html'
	title='Class Message'
	
	def get_initial(self, **kwargs):
		initial=super(ClasspageCreateView, self).get_initial()
		initial['klass']=Klass.objects.filter(name=self.kwargs['class_url'])
		return initial

	def form_valid(self, form):
	    new_classpage=form.save(commit=False)
	    new_classpage.date=date.today()
	    new_classpage.entered_by=self.request.user
	    new_classpage.save()
	    for k in form.cleaned_data['klass']:
	    	new_classpage.klass.add(k)

	    return HttpResponseRedirect(reverse('classpage-list-view', args=(self.kwargs['class_url'],)))

class ClasspageUpdateView(URLMixin, UpdateView):
    model=Classpage
    form_class=Classpage_ModifyForm
    template_name="generic/generic_modify.html"
    title='Class Message'
    
    def get_initial(self, **kwargs):
        initial=super(ClasspageUpdateView, self).get_initial()
        initial['klass']=self.object.klass.all()
        return initial

#	  Limits the choices of modelchoiceformfield
#     def get_form(self, form_class):
#         form=super(ClasspageUpdateView, self).get_form(form_class)
#         form.fields['klass'].queryset=self.object.klass.all()
#         return form

    def form_valid(self, form):
        new_classpage=form.save(commit=False)
        old_classpage=Classpage.objects.get(id=new_classpage.id)

        #DELETE
        #Removes klasses from object
        #if empty deletes the object
        if self.request.POST['mod/del']=='Delete':
            for k in form.cleaned_data['klass']:
            	new_classpage.klass.remove(k)
            if new_classpage.klass.exists():
            	new_classpage.save()
            else:
            	new_classpage.delete()

        #MODIFY
        #Removes selected classes from the object
        #IF empty deletes the object
        #Klasses being modified are removed those not changing are left alone
        else:
            for k in form.cleaned_data['klass']:
            	old_classpage.klass.remove(k)
            
            if old_classpage.klass.exists():
            	old_classpage.save()
            else:
            	old_classpage.delete()   
            
            new_classpage.id=None
            new_classpage.date=date.today()
            new_classpage.entered_by=self.request.user
            new_classpage.save()
            for k in form.cleaned_data['klass']:
            	new_classpage.klass.add(k)

        return HttpResponseRedirect(reverse('classpage-list-view', args=(self.kwargs['class_url'],)))
