from django.conf.urls import patterns, url
from homepage.views import HomepageListView, HomepageCreateView, HomepageUpdateView
from django.contrib.auth.decorators import user_passes_test

urlpatterns=patterns('homepage.views',
    url(r'^$', HomepageListView.as_view(), name='homepage-list-view'),
    url(r'^add/$', user_passes_test(lambda u:u.is_staff)(HomepageCreateView.as_view())),
    url(r'^modify/(?P<pk>\d+)/$', user_passes_test(lambda u:u.is_staff)(HomepageUpdateView.as_view())),


    )