from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from messages.models import Topic, Msg
from messages.forms import Add_Topic_Form, Add_Message_Form
from homework.models import Hwk_Details
from classlists.models import Klass
from datetime import datetime, date
from classpage.views import URLMixin

class TopicListView(URLMixin, ListView):
    template_name="topic_list.html"

    def get_queryset(self, **kwargs):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        return Topic.objects.all().order_by('-last_msg').filter(klass=klass)[:15]

class TopicCreateView(CreateView):
	model=Topic
	form_class=Add_Topic_Form
	template_name="generic/generic_form.html"
	title='Topic'
	
	def get_context_data(self, **kwargs):
	    context=super(TopicCreateView, self).get_context_data(**kwargs)
	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    context['form'].fields['hwk_details'].queryset=Hwk_Details.objects.filter(klass=klass)
	    context['klass']=klass
	    context['next']=self.request.path
	    return context

	def form_valid(self, form):
	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    new_topic=form.save(commit=False)
	    new_topic.last_msg=datetime.now()
	    new_topic.klass=klass
	    if form.cleaned_data['hwk_details']:
	        new_topic.homework=form.cleaned_data['hwk_details'].hwk
	    new_topic.save()
	    return HttpResponseRedirect(reverse('message_add_view', args=(self.kwargs['class_url'],new_topic.id,)))
 
class MessageListView(ListView):

	def get_queryset(self, **kwargs):
		topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
		return Msg.objects.filter(topic=topic).order_by('-entered_on').exclude(msg_replied_to__isnull=False)
 	
	def get_context_data(self, **kwargs):
	    context=super(MessageListView, self).get_context_data(**kwargs)
	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
	    context['topic']=topic
	    if topic.homework:
	        context['homework']=topic.homework.hwk_details_set.get(klass=klass)
	    context['klass']=klass
	    context['next']=self.request.path
	    return context

class MessageCreateView(CreateView):
    model=Msg
    form_class=Add_Message_Form
    
    def get_context_data(self, **kwargs):
        context=super(MessageCreateView, self).get_context_data(**kwargs)
        topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
        context['topic']=topic
        context['msg_list']=Msg.objects.filter(topic=topic).order_by('-entered_on').exclude(msg_replied_to__isnull=False)
        context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
        context['next']=self.request.path
        return context
        
    def form_valid(self, form):
        klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
        new_msg=form.save(commit=False)
        topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
        new_msg.topic=topic
        new_msg.entered_on=datetime.now()
        new_msg.author=self.request.user
        new_msg.klass=klass
        new_msg.save()
        
        topic_update=Topic(
                        id=topic.id,
                        topic=topic.topic,
                        homework=topic.homework,
                        last_msg=datetime.now(),
                        klass=klass,
                        )
        topic_update.save()
        return HttpResponseRedirect(reverse('message_view', args=(self.kwargs['class_url'],topic.id,)))



def DeleteMessageView(request, class_url, topic_id, message_id):
	##deletes all messages in thread including replies
	topic=Topic.objects.get(id=int(topic_id))
	m=Msg.objects.get(id=int(message_id))
	if (request.user == m.author) or (request.user.is_staff):
	    m.delete()
	return HttpResponseRedirect(reverse('message_view', args=(class_url,topic.id,)))

class ReplyMessageCreateView(CreateView):
	model=Msg
	form_class=Add_Message_Form
	template_name='messages/reply_message.html'
	
	def get_context_data(self, **kwargs):
	    context=super(ReplyMessageCreateView, self).get_context_data(**kwargs)
	    topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
	    context['topic']=topic
	    context['msg_replied_to']=Msg.objects.get(id=int(self.kwargs['message_id']))
	    context['msg_list']=Msg.objects.filter(topic=topic).order_by('-entered_on').exclude(msg_replied_to__isnull=False)
	    context['klass']=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    context['next']=self.request.path
	    return context
	    
	def form_valid(self, form):
	    klass=Klass.objects.get(klass_name=self.kwargs['class_url'])
	    
	    topic=Topic.objects.get(id=int(self.kwargs['topic_id']))
	    msg_replied_to=Msg.objects.get(id=int(self.kwargs['message_id']))
	    
	    reply_msg=form.save(commit=False)
	    reply_msg.topic=topic
	    reply_msg.entered_on=datetime.now()
	    reply_msg.msg_replied_to=msg_replied_to
	    reply_msg.author=self.request.user
	    reply_msg.klass=klass
	    reply_msg.save()
	    
	    topic_update=Topic(
	                    id=topic.id,
	                    topic=topic.topic,
	                    homework=topic.homework,
	                    last_msg=datetime.now(),
	                    klass=klass,
	                    )
	    topic_update.save()
	    return HttpResponseRedirect('/'+klass.klass_name+'/messages/'+str(topic.id)+'/messages')		
