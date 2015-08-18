from django.contrib import admin
from .models import Day_No, Period
from schoolsetup.models import Schedule_Setup

class PeriodInline(admin.TabularInline):
	model=Period
	extra=Schedule_Setup.objects.all()[0].periods_in_day

class Day_NoAdmin(admin.ModelAdmin):
	fields=['day_name','klass']
	list_display=('day_name','klass')
	inlines=[PeriodInline]

class PeriodAdmin(admin.ModelAdmin):
	list_display=('day_no','get_klass','details','activity','modified')
	list_filter=('day_no__day_name','day_no__klass','details')
	
	def get_klass(self, obj):
		return obj.day_no.klass.klass_name
	get_klass.short_description='Class'

admin.site.register(Day_No, Day_NoAdmin)
admin.site.register(Period, PeriodAdmin)
