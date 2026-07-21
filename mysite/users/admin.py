from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    extra = 0

# Unregister the default UserAdmin
admin.site.unregister(User)

# Define a new UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    # This controls the columns in the main list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')

    def get_role(self, obj):
        return getattr(obj.profile, 'role', 'customer')

    get_role.short_description = 'Role'

# Register the Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'location')
    list_filter = ('role',)