from django.contrib import admin
from messages.models import Topic,Msg

class MsgAdmin(admin.ModelAdmin):
        
    def queryset(self, request):
        qs=super(MsgAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(class_db=request.user.get_profile().in_class)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('msg_text','topic','author','class_db',)
        else:
            return ('msg_text','topic','author',)

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter=('author','class_db',)
        else:
            self.list_filter=('author',)
        return super(MsgAdmin, self).changelist_view(request, extra_context)

admin.site.register(Msg, MsgAdmin)

class TopicAdmin(admin.ModelAdmin):
        
    def queryset(self, request):
        qs=super(TopicAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(class_db=request.user.get_profile().in_class)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('topic','class_db',)
        else:
            return ('topic',)

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter=('class_db',)
        else:
            self.list_filter=None
        return super(TopicAdmin, self).changelist_view(request, extra_context)

admin.site.register(Topic, TopicAdmin)
