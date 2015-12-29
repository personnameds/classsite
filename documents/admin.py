from django.contrib import admin

from documents.models import Document

class DocumentAdmin(admin.ModelAdmin):
    list_display=('filename','description','subject','klass_list',)
    list_filter=('subject','klass',)
    
    def klass_list(self, obj):
        klass_list=[]
        for k in obj.klass.all():
            klass_list.append(k.name)
        return ', '.join(klass_list)
    klass_list.short_description='Classes'
    
admin.site.register(Document, DocumentAdmin)
