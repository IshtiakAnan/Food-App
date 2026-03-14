from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

# Unregister the default UserAdmin
admin.site.unregister(User)

# Define a new UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # This controls the columns in the main list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

# Register the Profile model
admin.site.register(Profile)