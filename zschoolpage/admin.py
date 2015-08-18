from django.contrib import admin
from schoolpage.models import Schoolpage

class SchoolpageAdmin(admin.ModelAdmin):
    ordering=("-date",)
    list_display=('message','date','entered_by_display',)
    list_filter=('entered_by__kksa_staff',)
    date_hierarchy='date'
    
admin.site.register(Schoolpage, SchoolpageAdmin)