from django.contrib import admin
from homework.models import Homework, Hwk_Details
import string

class HwkDetailsInline(admin.TabularInline):
    model=Hwk_Details

class HomeworkAdmin(admin.ModelAdmin):
    date_hierarchy='entered_on'
    list_display=('subject','work','klass_list','entered_by','entered_on')
    list_filter=('subject','hwk_details__klass',)
    inlines=[HwkDetailsInline,]

    def klass_list(self, obj):
        klass_list=[]
        for h in obj.hwk_details_set.all():
            klass_list.append(h.klass.name)
        return ', '.join(klass_list)
    klass_list.short_description='Classes' 

admin.site.register(Homework, HomeworkAdmin)
