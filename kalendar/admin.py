from django.contrib import admin

from .models import Kalendar

class KalendarAdmin(admin.ModelAdmin):
	fields=('date','day_no')
	list_display=('date','day_no')

admin.site.register(Kalendar, KalendarAdmin)
