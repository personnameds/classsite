from django.contrib import admin

from .models import Student, School_Staff, Klass, StaffCode


class StudentAdmin(admin.ModelAdmin):
	list_display=('full_name','user','klass')
	list_filter=('klass',)

admin.site.register(Student, StudentAdmin)


class School_StaffAdmin(admin.ModelAdmin):
	list_display=('teacher_name','user','allow_contact')
		
admin.site.register(School_Staff, School_StaffAdmin)

class KlassAdmin(admin.ModelAdmin):
	list_display=('name','code','url','schedule','teacher_list')
	list_filter=('schedule','teachers')
	
	def teacher_list(self, obj):
	    teacher_list=[]
	    for t in obj.teachers.all():
	        teacher_list.append(t.teacher_name)
	    return ', '.join(teacher_list)
	teacher_list.short_description='Teachers'
	
class StaffCodeAdmin(admin.ModelAdmin):
	list_display=('code',)

admin.site.register(Klass, KlassAdmin)
admin.site.register(StaffCode, StaffCodeAdmin)
