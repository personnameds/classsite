from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from classlists.models import UserProfile, Classes

class UserProfileInline(admin.StackedInline):
    model=UserProfile
    can_delete=False
    verbose_name_plural='profile'

class UserAdmin(UserAdmin):
    inlines=(UserProfileInline, )

    def queryset(self, request):
        qs=super(UserAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(userprofile__in_class=request.user.get_profile().in_class)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('username','first_name','last_name',)
        else:
            return ('username','first_name','last_name',)

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter=('userprofile__in_class',)
        else:
            self.list_filter=None
        return super(UserAdmin, self).changelist_view(request, extra_context)
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Classes)





