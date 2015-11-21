from django.contrib import admin

from .models import Kalendar, Day_No, Kalendar_Setup, Event

class KalendarAdmin(admin.ModelAdmin):
	fields=('date','day_no')
	list_display=('date','day_no')
	date_hierarchy='date'

class Day_NoAdmin(admin.ModelAdmin):
	fields=('day_name',)
	list_display=('day_name',)
	
class EventAdmin(admin.ModelAdmin):
    list_display=('event_date','description','klass_names')
    list_filter=('klass',)



admin.site.register(Day_No, Day_NoAdmin)
admin.site.register(Kalendar, KalendarAdmin)
admin.site.register(Kalendar_Setup)
admin.site.register(Event, EventAdmin)