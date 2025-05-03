from django.contrib import admin
from .models import Interview

class InterviewAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'get_candidate', 'get_job', 'interview_type', 
        'date_time', 'status', 'created_at'
    ]
    list_filter = ['interview_type', 'status', 'date_time']
    search_fields = [
        'application__candidate__username', 
        'application__job__title', 
        'notes', 'feedback'
    ]
    date_hierarchy = 'date_time'
    
    def get_candidate(self, obj):
        return obj.application.candidate.username
    get_candidate.short_description = 'Candidate'
    
    def get_job(self, obj):
        return obj.application.job.title
    get_job.short_description = 'Job'

admin.site.register(Interview, InterviewAdmin)
