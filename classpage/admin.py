from django.contrib import admin
from classpage.models import Classpage

class ClasspageAdmin(admin.ModelAdmin):
    ordering=("-date",)
    list_display=('message','date','klass','entered_by_display',)
    list_filter=('klass','entered_by__kksa_staff')
    date_hierarchy='date'
    
admin.site.register(Classpage, ClasspageAdmin)