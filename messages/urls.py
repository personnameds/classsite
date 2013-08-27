from django.conf.urls.defaults import patterns, include, url
from messages.views import TopicCreateView, MessageCreateView, MessageListView, ReplyMessageCreateView, TopicListView, DeleteMessageView

#from classsite3.feed import TopicsFeed

urlpatterns = patterns('',
	url(r'^$', TopicListView.as_view(), name='topic_view'),
 	url(r'^add_topic/$',TopicCreateView.as_view()),
	url(r'^(?P<topic_id>\d+)/messages/$',MessageListView.as_view(),name='message_view'),
	url(r'^(?P<topic_id>\d+)/add_message/$',MessageCreateView.as_view(),name='message_add_view'),
	url(r'^(?P<topic_id>\d+)/(?P<message_id>\d+)/reply/$',ReplyMessageCreateView.as_view()),	
	url(r'^(?P<topic_id>\d+)/(?P<message_id>\d+)/delete/$',DeleteMessageView),	
									
	)
