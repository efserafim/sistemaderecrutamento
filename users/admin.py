from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CandidateProfile, RecruiterProfile

# Customize the admin interface for the CustomUser model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role', 'phone', 'bio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role', 'phone', 'bio')}),
    )
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']

class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'experience']
    search_fields = ['user__username', 'user__email', 'skills']

class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'position']
    search_fields = ['user__username', 'user__email', 'company']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CandidateProfile, CandidateProfileAdmin)
admin.site.register(RecruiterProfile, RecruiterProfileAdmin)
