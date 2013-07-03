from django.conf.urls import patterns, url

from django.views.generic import TemplateView ##for testing only
from homepage.views import HomepageListView #, HomepageCreateView, HomepageUpdateView
# from django.contrib.auth.decorators import user_passes_test
# 

urlpatterns=patterns('',
#    url(r'^$', TemplateView.as_view(template_name="test.html")), # for testing only
    url(r'^$', HomepageListView.as_view(), name='homepage-list-view'),
#     url(r'^add/$', user_passes_test(lambda u:u.is_staff)(HomepageCreateView.as_view())),
#     url(r'^modify/(?P<pk>\d+)/$', user_passes_test(lambda u:u.is_staff)(HomepageUpdateView.as_view())),
# 
# 
     )