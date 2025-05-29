from django.db import models
from django.utils import timezone
from jobs.models import Application

class Interview(models.Model):
    """Model for scheduling interviews with candidates"""
    class InterviewType(models.TextChoices):
        PHONE = 'PHONE', 'Entrevista por Telefone'
        VIDEO = 'VIDEO', 'Chamada de Vídeo'
        IN_PERSON = 'IN_PERSON', 'Entrevista Presencial'
        TECHNICAL = 'TECHNICAL', 'Avaliação Técnica'

    
    class InterviewStatus(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Agendado'
        COMPLETED = 'COMPLETED', 'Concluído'
        CANCELED = 'CANCELED', 'Cancelado'
        RESCHEDULED = 'RESCHEDULED', 'Remarcado'
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    interview_type = models.CharField(max_length=20, choices=InterviewType.choices)
    date_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    location = models.CharField(max_length=255, blank=True, null=True, 
                               help_text="Physical location or meeting link")
    status = models.CharField(max_length=20, choices=InterviewStatus.choices, default=InterviewStatus.SCHEDULED)
    notes = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_interview_type_display()} for {self.application.candidate.username}"
    
    @property
    def recruiter(self):
        return self.application.job.recruiter
    
    @property
    def candidate(self):
        return self.application.candidate
    
    @property
    def job(self):
        return self.application.job
    
    @property
    def is_past(self):
        return self.date_time < timezone.now()
    
    class Meta:
        ordering = ['date_time']
