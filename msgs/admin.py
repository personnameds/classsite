from django.contrib import admin
from .models import Topic,Msg

class MsgAdmin(admin.ModelAdmin):
    list_display=('msg_text','topic','author','klass',)
    list_filter=('author','klass',)

class TopicAdmin(admin.ModelAdmin):
    list_display=('topic','klass',)
    list_filter=('klass',)

admin.site.register(Topic, TopicAdmin)
admin.site.register(Msg, MsgAdmin)