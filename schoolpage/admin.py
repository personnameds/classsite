from django.contrib import admin
from schoolpage.models import Schoolpage

class SchoolpageAdmin(admin.ModelAdmin):
    ordering=("-date",)
    list_display=('message','date','entered_by',)
    list_filter=('entered_by',)
    date_hierarchy='date'
    
admin.site.register(Schoolpage, SchoolpageAdmin)