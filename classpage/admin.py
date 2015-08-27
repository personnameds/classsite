from django.contrib import admin
from classpage.models import Classpage

class ClasspageAdmin(admin.ModelAdmin):
    list_display=('message','date','klass','entered_by_display',)
    list_filter=('klass','entered_by__school_staff',)
    date_hierarchy='date'
    
admin.site.register(Classpage, ClasspageAdmin)

