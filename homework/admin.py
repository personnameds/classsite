from django.contrib import admin
from homework.models import Homework, Hwk_Details
import string

class HwkDetailsInline(admin.TabularInline):
    model=Hwk_Details

class HomeworkAdmin(admin.ModelAdmin):
    date_hierarchy='entered_on'
    list_display=('subject_list','work_list','klass_list')
    #list_filter=('subject',)
    inlines=[HwkDetailsInline,]

    def klass_list(self, obj):
        klass_list=[]
        for h in obj.hwk_details_set.all():
            klass_list.append(h.klass.klass_name)
        return string.join(klass_list,', ')
    klass_list.short_description='Classes' 

    def subject_list(self, obj):
        subject_list=[]
        for s in obj.hwk_details_set.all().values_list('subject', flat=True).distinct():
            subject_list.append(s)
        return string.join(subject_list,', ')
    subject_list.short_description='Subject'

    def work_list(self, obj):
        work_list=[]
        for s in obj.hwk_details_set.all().values_list('assigned_work', flat=True).distinct():
            work_list.append(s)
        return string.join(work_list,', ')
    work_list.short_description='Assigned_Work'

admin.site.register(Homework, HomeworkAdmin)
