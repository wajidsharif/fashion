from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    min_num = 1
    max_num = 1


class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_mobile', 'is_active']
    list_select_related = ['profile']

    def get_mobile(self, instance):
        try:
            return instance.profile.mobile
        except UserProfile.DoesNotExist:
            return ''
    get_mobile.short_description = 'Mobile'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        UserProfile.objects.get_or_create(user=form.instance)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
