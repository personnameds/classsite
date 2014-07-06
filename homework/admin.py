from django.contrib import admin
from homework.models import Homework

class HomeworkAdmin(admin.ModelAdmin):
    date_hierarchy='entered_on'
    list_display=('subject','assigned_work','due_date','klass_names',)
    list_filter=('klass','subject',)

admin.site.register(Homework, HomeworkAdmin)