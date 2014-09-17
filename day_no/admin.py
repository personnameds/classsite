from django.contrib import admin
from day_no.models import Day_No

class Day_NoAdmin(admin.ModelAdmin):
    list_filter=('klass',)
    list_display=('day_name','klass',)
    
admin.site.register(Day_No, Day_NoAdmin)


