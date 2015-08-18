from django.contrib import admin
from links.models import Link
import string

class LinksAdmin(admin.ModelAdmin):
    list_display=('subject','link', 'description','klass_list',)
    list_filter=('subject',)

    def klass_list(self, obj):
        klass_list=[]
        for k in obj.klass.all():
            klass_list.append(k.klass_name)
        return string.join(klass_list,', ')
    klass_list.short_description='Classes' 

admin.site.register(Link, LinksAdmin)


