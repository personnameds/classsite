from django.contrib import admin
from links.models import Link

class LinksAdmin(admin.ModelAdmin):



    def get_list_display(self, request):
        return ('link','description','klass',)


    def changelist_view(self, request, extra_context=None):
        self.list_filter=('klass',)
        return super(LinksAdmin, self).changelist_view(request, extra_context)

admin.site.register(Link, LinksAdmin)
