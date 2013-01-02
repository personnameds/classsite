from django.contrib import admin
from links.models import Link

from django.contrib import admin
from documents.models import Document

class LinksAdmin(admin.ModelAdmin):

    def queryset(self, request):
        qs=super(LinksAdmin, self).queryset(request)
        
        if request.user.is_superuser:
            return qs
        return qs.filter(class_db=request.user.get_profile().in_class)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('link','description','class_db',)
        else:
            return ('link','description',)

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter=('class_db',)
        else:
            self.list_filter=None
        return super(LinksAdmin, self).changelist_view(request, extra_context)

admin.site.register(Link, LinksAdmin)
