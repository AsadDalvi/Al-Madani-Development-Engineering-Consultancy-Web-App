from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Inquiry, Feedback, FloorPlan, Gallery  # Import all models

# Define the admin class for CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')  # Display role, staff, and active status
    list_filter = ('role', 'is_staff', 'is_active')  # Adding filters for role, staff, and active status
    search_fields = ('username', 'email')  # Enabling search by username and email
    ordering = ('username',)  # Order users alphabetically by username

    # Fields to display in the user detail page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role & Status', {'fields': ('role',)}),  # Include role field
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),  
    )

    # Fields when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        }),
        ('Role & Status', {'fields': ('role',)}),  # Add role field
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), 
    )

# Registering the models with the Django admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Inquiry)
admin.site.register(Feedback)
admin.site.register(FloorPlan)
admin.site.register(Gallery)
