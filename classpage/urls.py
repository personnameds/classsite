from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required
from .views import ClasspageListView, ClasspageCreateView, ClasspageUpdateView

urlpatterns = [
    url(r'^$', ClasspageListView.as_view(), name='classpage-list-view'),
    url(r'^(?i)add/$', permission_required('classpage.add_classpage')(ClasspageCreateView.as_view()), name='classpage-create-view'),
    url(r'^(?i)modify/(?P<pk>\d+)/$', permission_required('classpage.change_classpage')(ClasspageUpdateView.as_view()), name='classpage-update-view'),

]

