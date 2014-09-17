from django.conf.urls import patterns, include, url
from messages.views import TopicCreateView, MessageCreateView, MessageListView, ReplyMessageCreateView, TopicListView, DeleteMessageView
from django.contrib.auth.decorators import login_required
#from classsite3.feed import TopicsFeed

urlpatterns = patterns('',
	url(r'^$', login_required(login_url='/registration/login/')(TopicListView.as_view()), name='topic_view'),
 	url(r'^add_topic/$',login_required(login_url='/registration/login/')(TopicCreateView.as_view())),
	url(r'^(?P<topic_id>\d+)/messages/$',login_required(login_url='/registration/login/')(MessageListView.as_view()),name='message_view'),
	url(r'^(?P<topic_id>\d+)/add_message/$',login_required(login_url='/registration/login/')(MessageCreateView.as_view()),name='message_add_view'),
	url(r'^(?P<topic_id>\d+)/(?P<message_id>\d+)/reply/$',login_required(login_url='/registration/login/')(ReplyMessageCreateView.as_view())),	
	url(r'^(?P<topic_id>\d+)/(?P<message_id>\d+)/delete/$',login_required(login_url='/registration/login/')(DeleteMessageView)),	
									
	)
