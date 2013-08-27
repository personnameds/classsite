from django.contrib import admin
from documents.models import Document

class DocumentAdmin(admin.ModelAdmin):


    def get_list_display(self, request):
        return ('filename','klass',)

    def changelist_view(self, request, extra_context=None):
        self.list_filter=('klass',)
        return super(DocumentAdmin, self).changelist_view(request, extra_context)

admin.site.register(Document, DocumentAdmin)





