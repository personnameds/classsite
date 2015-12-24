from django.conf.urls import url
from .views import TopicCreateView, MessageCreateView, MessageListView, ReplyMessageCreateView, TopicListView, DeleteMessageView
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$', login_required()(TopicListView.as_view()), name='topic-list-view'),
 	url(r'^add_topic/$',login_required()(TopicCreateView.as_view()), name='topic-create-view'),
	url(r'^(?P<topic_id>\d+)/add_message/$',login_required()(MessageCreateView.as_view()),name='message-create-view'),
	url(r'^(?P<topic_id>\d+)/messages/$',login_required()(MessageListView.as_view()),name='message-list-view'),
	url(r'^(?P<topic_id>\d+)/(?P<message_id>\d+)/reply/$',login_required()(ReplyMessageCreateView.as_view()),name='reply-message-view'),	
	url(r'^(?P<topic_id>\d+)/(?P<message_id>\d+)/delete/$',login_required()(DeleteMessageView),name='delete-message-view'),	
									
	]

