# from django.contrib import admin
# from homepage.models import Homepage
# 
# class HomepageAdmin(admin.ModelAdmin):
#     ordering=("-date",)
#     list_display=('message','date','class_db','entered_by',)
#     
#     def queryset(self, request):
#         qs=super(HomepageAdmin, self).queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(class_db=request.user.get_profile().in_class)
# 
#     def get_list_display(self, request):
#         if request.user.is_superuser:
#             return ('message','date','class_db','entered_by',)
#         else:
#             return ('message','date','entered_by',)
# 
#     def changelist_view(self, request, extra_context=None):
#         if request.user.is_superuser:
#             self.list_filter=('class_db',)
#         else:
#             self.list_filter=None
#         return super(HomepageAdmin, self).changelist_view(request, extra_context)
#     
# admin.site.register(Homepage, HomepageAdmin)