from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import Topic, Msg, Add_TopicForm, Add_MessageForm
from homework.models import Hwk_Details
from classlists.models import Klass
from datetime import datetime, date
from classsite.views import URLMixin

class TopicListView(URLMixin, ListView):
    template_name="topic_list.html"

    def get_queryset(self, **kwargs):
        klass=Klass.objects.get(name=self.kwargs['class_url'])
        return Topic.objects.all().order_by('-last_msg').filter(klass=klass)[:15]

class TopicCreateView(URLMixin, CreateView):
	model=Topic
	form_class=Add_TopicForm
	template_name="generic/generic_form.html"
	title='Topic'
	named_url='topic-create-view'

	def get_context_data(self, **kwargs):
	    klass=Klass.objects.get(name=self.kwargs['class_url'])
	    context=super(TopicCreateView, self).get_context_data(**kwargs)
	    context['form'].fields['hwk_details'].queryset=Hwk_Details.objects.filter(klass=klass).exclude(due_date__date__lt=(date.today())).prefetch_related().order_by('due_date')
	    return context

	def form_valid(self, form):
	    klass=Klass.objects.get(name=self.kwargs['class_url'])
	    new_topic=form.save(commit=False)
	    new_topic.last_msg=datetime.now()
	    new_topic.klass=klass
	    if form.cleaned_data['hwk_details']:
	        new_topic.homework=form.cleaned_data['hwk_details'].homework
	    new_topic.save()
	    return HttpResponseRedirect(reverse('message-create-view', args=(self.kwargs['class_url'],new_topic.id,)))
 
class MessageListView(URLMixin, ListView):

	def get_queryset(self, **kwargs):
		topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
		return Msg.objects.filter(topic=topic).order_by('-entered_on').exclude(msg_replied_to__isnull=False)
 	
	def get_context_data(self, **kwargs):
	    context=super(MessageListView, self).get_context_data(**kwargs)
	    klass=Klass.objects.get(name=self.kwargs['class_url'])
	    topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
	    context['topic']=topic
	    if topic.homework:
	        context['homework']=topic.homework.hwk_details_set.get(klass=klass)
	    return context

class MessageCreateView(URLMixin, CreateView):
    model=Msg
    form_class=Add_MessageForm
    
    def get_context_data(self, **kwargs):
        context=super(MessageCreateView, self).get_context_data(**kwargs)
        topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
        context['topic']=topic
        context['msg_list']=Msg.objects.filter(topic=topic).order_by('-entered_on').exclude(msg_replied_to__isnull=False)
        return context
        
    def form_valid(self, form):
        klass=Klass.objects.get(name=self.kwargs['class_url'])
        new_msg=form.save(commit=False)
        topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
        new_msg.topic=topic
        new_msg.entered_on=datetime.now()
        new_msg.author=self.request.user
        new_msg.klass=klass
        new_msg.save()
        
        topic.last_msg=datetime.now()
        topic.save()
        
        return HttpResponseRedirect(reverse('message-list-view', args=(self.kwargs['class_url'],topic.id,)))

def DeleteMessageView(request, class_url, topic_id, message_id):
	##deletes all messages in thread including replies
	m=Msg.objects.get(id=int(message_id))
	m.delete()
	return HttpResponseRedirect(reverse('message-list-view', args=(class_url,topic_id,)))

class ReplyMessageCreateView(URLMixin, CreateView):
	model=Msg
	form_class=Add_MessageForm
	template_name='msgs/reply_message.html'
	
	def get_context_data(self, **kwargs):
	    context=super(ReplyMessageCreateView, self).get_context_data(**kwargs)
	    topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
	    context['topic']=topic
	    context['msg_replied_to']=Msg.objects.get(id=int(self.kwargs['message_id']))
	    context['msg_list']=Msg.objects.filter(topic=topic).order_by('-entered_on').exclude(msg_replied_to__isnull=False)
	    return context
	    
	def form_valid(self, form):
	    klass=Klass.objects.get(name=self.kwargs['class_url'])
	    
	    topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
	    msg_replied_to=Msg.objects.get(id=int(self.kwargs['message_id']))
	    
	    reply_msg=form.save(commit=False)
	    reply_msg.topic=topic
	    reply_msg.entered_on=datetime.now()
	    reply_msg.msg_replied_to=msg_replied_to
	    reply_msg.author=self.request.user
	    reply_msg.klass=klass
	    reply_msg.save()
	    
	    topic_update=last_msg=datetime.now(),
	    topic.save()
	    return HttpResponseRedirect(reverse('message-list-view', args=(self.kwargs['class_url'],topic.id,)))		
