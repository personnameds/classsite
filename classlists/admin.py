from django.contrib import admin

from classlists.models import Klass, KKSA_Staff, Student

class KlassAdmin(admin.ModelAdmin):
    list_display=('klass_name','teacher','class_code')
    readonly_fields = ('banner_tag',)

class StudentAdmin(admin.ModelAdmin):
    list_display=('full_name','student','klass',)
    list_filter=('klass',)

admin.site.register(Klass, KlassAdmin)
admin.site.register(KKSA_Staff)
admin.site.register(Student, StudentAdmin)