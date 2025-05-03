from django.contrib import admin
from .models import Job, Application

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'recruiter', 'created_at', 'is_active']
    list_filter = ['job_type', 'is_active', 'created_at']
    search_fields = ['title', 'company', 'location', 'description', 'recruiter__username']
    list_editable = ['is_active']
    date_hierarchy = 'created_at'

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'status', 'applied_at', 'updated_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['candidate__username', 'job__title', 'recruiter_notes']
    date_hierarchy = 'applied_at'
    raw_id_fields = ['candidate', 'job']

admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
