from django.contrib import admin
from .models import Period_Details, Period_Activity, Schedule_Setup

#TO DO Create inline admin fields

class PeriodDetailsInline(admin.TabularInline):
    model=Period_Details
    
class Schedule_SetupAdmin(admin.ModelAdmin):
    list_display=('name','periods_in_day')
    inlines=[PeriodDetailsInline,]

class Period_ActivityAdmin(admin.ModelAdmin):
	fields=('details','klass','activity','day_no','org','del_date',)
	list_display=('details','klass','activity','day_no','org','del_date')
	list_filter=('klass','day_no',)

admin.site.register(Period_Activity,Period_ActivityAdmin)
admin.site.register(Schedule_Setup, Schedule_SetupAdmin)
admin.site.register(Period_Details)
