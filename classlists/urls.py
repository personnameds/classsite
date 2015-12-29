from django.conf.urls import url
from .views import ClasslistsView, StudentUpdateView, StudentCreateView
from django.contrib.auth.decorators import permission_required

urlpatterns = [
	url(r'^$', ClasslistsView.as_view(),name='classlists-view'),
	url(r'^(?i)studentcreate/$', permission_required('classlists.add_student')(StudentCreateView.as_view()),name='student-create-view'),
	url(r'^(?i)studentupdate/(?P<pk>\d+)/$', permission_required('classlists.change_student')(StudentUpdateView.as_view()),name='student-update-view'),
	]
