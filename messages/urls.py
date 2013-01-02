from django.conf.urls.defaults import patterns, include, url
from messages.views import TopicCreateView, MessageCreateView, MessageListView, ReplyMessageCreateView, TopicListView, DeleteMessageView
from django.contrib.auth.decorators import login_required
#from classsite3.feed import TopicsFeed

urlpatterns = patterns('',
	url(r'^$', TopicListView.as_view(), name='topic-list-view'),
 	url(r'^add_topic/$',login_required(TopicCreateView.as_view())),
	url(r'^(?P<topic_id>\d+)/messages/$',MessageListView.as_view(),name='message-list-view'),
	url(r'^(?P<topic_id>\d+)/add_message/$',login_required(MessageCreateView.as_view()),name='message-add-view'),
	url(r'^(?P<topic_id>\d+)/(?P<message_id>\d+)/reply/$',login_required(ReplyMessageCreateView.as_view())),	
	url(r'^(?P<topic_id>\d+)/(?P<message_id>\d+)/delete/$',login_required(DeleteMessageView)),	
									
	)
