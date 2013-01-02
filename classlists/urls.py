from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import permission_required
from classlists.views import AddClassCreateView

urlpatterns = patterns('',
	url(r'^$', permission_required('classes.add_classes')(AddClassCreateView.as_view())),									
	)
	