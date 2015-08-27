from django.contrib import admin

from .models import Student, School_Staff, Klass


class StudentAdmin(admin.ModelAdmin):
	list_display=('full_name','user','klass')
	list_filter=('klass',)

admin.site.register(Student, StudentAdmin)


class School_StaffAdmin(admin.ModelAdmin):
	list_display=('teacher_name','user','allow_contact')
		
admin.site.register(School_Staff, School_StaffAdmin)

class KlassAdmin(admin.ModelAdmin):
	list_display=('name','code','url')

admin.site.register(Klass, KlassAdmin)

