from django.contrib import admin
from homepage.models import Homepage

class HomepageAdmin(admin.ModelAdmin):
    ordering=("-date",)
    list_display=('message','date','klass','entered_by_display',)
    list_filter=('klass','entered_by__kksa_staff')
    date_hierarchy='date'
    
admin.site.register(Homepage, HomepageAdmin)