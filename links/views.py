from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from links.models import Link, Add_Link_Form
from classlists.models import Klass
from homework.models import Homework
from django.core.urlresolvers import reverse

from datetime import date, timedelta

class LinkListView(ListView):
    template_name="link_list.html"
    
    def get_queryset(self):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        return Link.objects.select_related().filter(klass=klass)
    
    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context=super(LinkListView, self).get_context_data(**kwargs)
        context['klass']=klass
        context['path']=self.request.path

        links_list=Link.objects.select_related().filter(klass=klass)
        subjects=links_list.values_list('subject', flat=True).distinct()
        context['subject_list']=subjects
        return context



class LinkCreateView(CreateView):
	model=Link
	form_class=Add_Link_Form
	template_name='links/link_form.html'
	
# 	def get_initial(self, **kwargs):
# 	    initial=super(LinkCreateView, self).get_initial()
# 	    class_url=self.kwargs['class_url']
# 	    class_db=Classes.objects.filter(classes=self.kwargs['class_url'])
# 	    initial['class_db']=class_db
# 	    return initial
	
	def get_context_data(self, **kwargs):
	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    context=super(LinkCreateView, self).get_context_data(**kwargs)
	    context['form'].fields['homework'].queryset=Homework.objects.exclude(due_date__date__lt=(date.today())).filter(klass=klass)
	    context['klass']=klass
	    context['path']=self.request.path
	    return context
	
  	def form_valid(self, form):
  	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
  	    new_link=form.save(commit=False)
  	    if new_link.subject==None:
  	        new_link.subject='Other'
  	    new_link.save()
  	    new_link.klass.add(klass)
  	    return HttpResponseRedirect(reverse('link_view', args=(self.kwargs['class_url'],),))


class LinkUpdateView(UpdateView):
    model=Link
    form_class=Add_Link_Form
    template_name="links/modify_link.html"

    def get_context_data(self, **kwargs):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context=super(LinkUpdateView, self).get_context_data(**kwargs)
        context['klass']=klass
        context['path']=self.request.path
        return context
        
    def form_valid(self, form):
        pk=self.kwargs['pk']
        new_link=Link.objects.get(id=pk)
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        if self.request.POST['mod/del']=='Delete':
            new_link.delete()
        else:
            new_link=form.save()
            new_link.klass.add(klass)
        return HttpResponseRedirect(reverse('link_view', args=(self.kwargs['class_url'],),))
            

