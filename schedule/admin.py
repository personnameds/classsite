from django.contrib import admin
from .models import Period_Details, Day_No, Period_Activity

#TO DO Create inline admin fields

class Period_DetailsAdmin(admin.ModelAdmin):
	fields=('number','name','start_time','end_time')
	list_display=('number','name','start_time','end_time')	

class Day_NoAdmin(admin.ModelAdmin):
	fields=('day_name',)
	list_display=('day_name',)

class Period_ActivityAdmin(admin.ModelAdmin):
	fields=('details','klass','activity','day_no','org')
	list_display=('details','klass','activity','day_no','org')

admin.site.register(Period_Activity,Period_ActivityAdmin)
admin.site.register(Period_Details, Period_DetailsAdmin)
admin.site.register(Day_No, Day_NoAdmin)


