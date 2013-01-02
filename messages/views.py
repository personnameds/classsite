from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from messages.models import Topic, Add_Topic_Form, Msg, Add_Message_Form
from homework.models import Homework
from classlists.models import Classes
from datetime import datetime, date

class TopicListView(ListView):
    template_name="topic_list.html"

    def get_queryset(self, **kwargs):
        class_db=Classes.objects.get(classes=self.kwargs['class_url'])
        return Topic.objects.all().order_by('last_msg').filter(class_db=class_db)[:15]
        
    def get_context_data(self, **kwargs):
	    class_url=self.kwargs['class_url']
	    context=super(TopicListView, self).get_context_data(**kwargs)
	    context['class_url']=class_url.lower()
	    return context

class TopicCreateView(CreateView):
	model=Topic
	form_class=Add_Topic_Form
	template_name="messages/topic_form.html"

	def get_context_data(self, **kwargs):
		class_url=self.kwargs['class_url']
		context=super(TopicCreateView, self).get_context_data(**kwargs)
		context['homework']=Homework.objects.exclude(due_date__date__lt=(date.today()))
		context['class_url']=class_url.lower()
		return context

  	def form_valid(self, form):
  	    class_url=self.kwargs['class_url']
  	    class_db=Classes.objects.get(classes=class_url)
  	    new_topic=form.save(commit=False)
  	    new_topic.last_msg=datetime.now()
  	    new_topic.class_db=class_db
  	    new_topic.save()
  	    return HttpResponseRedirect(reverse_lazy('message-add-view', args=(self.kwargs['class_url'],new_topic.id,)))
           

class MessageListView(ListView):

	def get_queryset(self, **kwargs):
		topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
		return Msg.objects.filter(topic=topic).order_by('-entered_on').exclude(msg_replied_to__isnull=False)
 	
	def get_context_data(self, **kwargs):
		class_url=self.kwargs['class_url']
		context=super(MessageListView, self).get_context_data(**kwargs)
		topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
		context['topic']=topic
		context['class_url']=class_url.lower()
		return context

class MessageCreateView(CreateView):
	model=Msg
	form_class=Add_Message_Form

	def get_context_data(self, **kwargs):
		class_url=self.kwargs['class_url']
		context=super(MessageCreateView, self).get_context_data(**kwargs)
		topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
		context['topic']=topic
		context['msg_list']=Msg.objects.filter(topic=topic).order_by('-entered_on').exclude(msg_replied_to__isnull=False)
		context['class_url']=class_url.lower()
		return context
	
	def form_valid(self, form):
		class_url=self.kwargs['class_url']
		class_db=Classes.objects.get(classes=class_url)
		new_msg=form.save(commit=False)
		topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
		new_msg.topic=topic
		new_msg.entered_on=datetime.now()
		new_msg.author=self.request.user
		new_msg.class_db=class_db
		new_msg.save()
		
		topic_update=Topic(
						id=topic.id,
						topic=topic.topic,
						homework=topic.homework,
						last_msg=datetime.now(),
						class_db=class_db,
						)
		topic_update.save()	
		return HttpResponseRedirect(reverse_lazy('message-list-view', args=(self.kwargs['class_url'],topic.id,)))



def DeleteMessageView(request, class_url, topic_id, message_id):
	##deletes all messages in thread including replies
	topic=Topic.objects.get(id=int(topic_id))
	m=Msg.objects.get(id=int(message_id))
	if (request.user == m.author) or (request.user.is_staff):
	    m.delete()
	return HttpResponseRedirect(reverse_lazy('message-list-view', args=(class_url,topic.id,)))

class ReplyMessageCreateView(CreateView):
	model=Msg
	form_class=Add_Message_Form
	template_name='messages/reply_message.html'

	def get_context_data(self, **kwargs):
		class_url=self.kwargs['class_url']
		context=super(ReplyMessageCreateView, self).get_context_data(**kwargs)
		topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
		context['topic']=topic
		context['msg_replied_to']=Msg.objects.get(id=int(self.kwargs['message_id']))
		context['msg_list']=Msg.objects.filter(topic=topic).order_by('-entered_on').exclude(msg_replied_to__isnull=False)
		context['class_url']=class_url.lower()
		return context
	
	def form_valid(self, form):
		class_url=self.kwargs['class_url']
		class_db=Classes.objects.get(classes=class_url)
		
		topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
		msg_replied_to=Msg.objects.get(id=int(self.kwargs['message_id']))

		reply_msg=form.save(commit=False)
		reply_msg.topic=topic
		reply_msg.entered_on=datetime.now()
		reply_msg.msg_replied_to=msg_replied_to
		reply_msg.author=self.request.user
		reply_msg.class_db=class_db
		reply_msg.save()
		
		topic_update=Topic(
						id=topic.id,
						topic=topic.topic,
						homework=topic.homework,
						last_msg=datetime.now(),
						class_db=class_db,
						)
		topic_update.save()
  		return HttpResponseRedirect('/'+class_url+'/messages/'+str(topic.id)+'/messages')		
