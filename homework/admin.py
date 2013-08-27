from django.contrib import admin
from homework.models import Homework

class HomeworkAdmin(admin.ModelAdmin):
    date_hierarchy='entered_on'

    def get_list_display(self, request):
        return ('subject','assigned_work','klass',)


    def changelist_view(self, request, extra_context=None):
        self.list_filter=('klass','subject')
        return super(HomeworkAdmin, self).changelist_view(request, extra_context)

admin.site.register(Homework, HomeworkAdmin)