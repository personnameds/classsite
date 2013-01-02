from django.contrib import admin
from homework.models import Homework

class HomeworkAdmin(admin.ModelAdmin):
    date_hierarchy='entered_on'
        
    def queryset(self, request):
        qs=super(HomeworkAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(class_db=request.user.get_profile().in_class)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('subject','assigned_work','class_db',)
        else:
            return ('subject','assigned_work',)

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter=('class_db','subject')
        else:
            self.list_filter=('subject',)
        return super(HomeworkAdmin, self).changelist_view(request, extra_context)

admin.site.register(Homework, HomeworkAdmin)