from django.contrib import admin
from kalendar.models import Kalendar, Event
from day_no.models import Day_No


class KalendarAdmin(admin.ModelAdmin):
    date_hierarchy='date'
    list_display=('date','day_no','mod_klasses',)

admin.site.register(Kalendar, KalendarAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display=('event_date','description','klass_names','kksa',)
    list_filter=('klass',)

admin.site.register(Event, EventAdmin)
