from django.contrib import admin
from day_no.models import Day_No

class Day_NoAdmin(admin.ModelAdmin):
    
    def queryset(self, request):
        qs=super(Day_NoAdmin, self).queryset(request)
        return qs

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('day_no','klass',)
        else:
            return ('day_no',)

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter=('klass',)
        else:
            self.list_filter=None
        return super(Day_NoAdmin, self).changelist_view(request, extra_context)


admin.site.register(Day_No, Day_NoAdmin)


