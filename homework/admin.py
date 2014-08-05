from django.contrib import admin
from homework.models import Homework, Hwk_Details
import string

class HwkDetailsInline(admin.TabularInline):
    model=Hwk_Details

class HomeworkAdmin(admin.ModelAdmin):
    date_hierarchy='entered_on'
    list_display=('subject','assigned_work','klass_list')
    list_filter=('subject',)
    inlines=[HwkDetailsInline,] 

    def klass_list(self, obj):
        klass_list=[]
        for hwk_detail in obj.hwk_details_set.all():
            klass_list.append(hwk_detail.klass.klass_name)
        return string.join(klass_list,', ')
    klass_list.short_description='Classes' 

admin.site.register(Homework, HomeworkAdmin)