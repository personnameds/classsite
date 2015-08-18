from django.contrib import admin

from .models import Period_Details, Schedule_Setup, Recess_Details


class PeriodInline(admin.TabularInline):
	model=Period_Details
	extra=1

class RecessInline(admin.TabularInline):
	model=Recess_Details
	extra=1

class Schedule_SetupAdmin(admin.ModelAdmin):
	#fields=('days_in_cycle',('before_start','before_end'))
	fieldsets=[
		(None, {'fields':['days_in_cycle','periods_in_day']}),
		('Before School',{'fields':['before_start','before_end']}),
		('Lunch',{'fields':['lunch_start','lunch_end']}),
		('After School',{'fields':['after_start','after_end']}),		
		]
	inlines=[PeriodInline, RecessInline]

class Period_DetailsAdmin(admin.ModelAdmin):
	list_display=('number','start_time','end_time')

class Recess_DetailsAdmin(admin.ModelAdmin):
	list_display=('number','start_time','end_time')
	
admin.site.register(Schedule_Setup, Schedule_SetupAdmin)
admin.site.register(Period_Details, Period_DetailsAdmin)
admin.site.register(Recess_Details, Recess_DetailsAdmin)

