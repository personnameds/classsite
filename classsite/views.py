from django.shortcuts import get_object_or_404
from classlists.models import Klass

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
		context=super(URLMixin, self).get_context_data(**kwargs)
		context['klass']=self.get_klass()
		context['next']=self.get_next()
		return context
