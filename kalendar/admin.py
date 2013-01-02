from django.contrib import admin
from kalendar.models import Kalendar, Event
from day_no.models import Day_No


class KalendarAdmin(admin.ModelAdmin):
    date_hierarchy='date'
    
    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('date','day_no',)
        else:
            return ('date','day_no',)

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter=None
        else:
            self.list_filter=None
        return super(KalendarAdmin, self).changelist_view(request, extra_context)

admin.site.register(Kalendar, KalendarAdmin)




class EventAdmin(admin.ModelAdmin):
    
    def queryset(self, request):
        qs=super(EventAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(class_db=request.user.get_profile().in_class)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('description','event_date','class_db',)
        else:
            return ('description','event_date',)

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter=('class_db',)
        else:
            self.list_filter=None
        return super(EventAdmin, self).changelist_view(request, extra_context)


admin.site.register(Event, EventAdmin)





