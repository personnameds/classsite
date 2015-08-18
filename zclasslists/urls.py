from django.conf.urls import patterns, include, url
from classlists.views import Class_Details_ListView, Staff_Edit_UpdateView, Code_Edit_UpdateView, Student_Edit_UpdateView
from django.contrib.auth.decorators import permission_required, login_required

urlpatterns = patterns('',
	url(r'^$',permission_required('classlists.is_kksastaff', 
					login_url='/registration/login/')(Class_Details_ListView.as_view()), 
					name='class-list-view',
					),
	url(r'^staff_edit/$',permission_required('classlists.is_kksastaff', 
					login_url='/registration/login/')(Staff_Edit_UpdateView.as_view()),
					name='class-staff-edit-view',
					),
	url(r'^code_edit/$',permission_required('classlists.is_kksastaff', 
					login_url='/registration/login/')(Code_Edit_UpdateView.as_view()),
					name='code-edit-view',
					),
	url(r'^student_edit/(?P<pk>\d+)/$',permission_required('classlists.is_kksastaff', 
					login_url='/registration/login/')(Student_Edit_UpdateView.as_view()),
					name='student-edit-view',
					),
	)