from django.contrib import admin
from messages.models import Topic,Msg

class MsgAdmin(admin.ModelAdmin):
        
    def get_list_display(self, request):
        return ('msg_text','topic','author','klass',)


    def changelist_view(self, request, extra_context=None):
        self.list_filter=('author','klass',)
        return super(MsgAdmin, self).changelist_view(request, extra_context)

admin.site.register(Msg, MsgAdmin)

class TopicAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        return ('topic','klass',)


    def changelist_view(self, request, extra_context=None):
        self.list_filter=('klass',)
        return super(TopicAdmin, self).changelist_view(request, extra_context)

admin.site.register(Topic, TopicAdmin)
