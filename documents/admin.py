from django.contrib import admin
from documents.models import Document

class DocumentAdmin(admin.ModelAdmin):
    list_display=('filename','description','subject','klass_list',)
    list_filter=('klass','subject')

admin.site.register(Document, DocumentAdmin)
