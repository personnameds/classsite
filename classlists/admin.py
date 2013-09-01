from django.contrib import admin

from classlists.models import Klass, Teacher#, Student

# class StudentAdmin(admin.ModelAdmin):
#     list_display=('user','klass',)
#     list_filter=('klass',)
# 
# admin.site.register(Student, StudentAdmin)
admin.site.register(Klass)
admin.site.register(Teacher)
