from django.db import models
from django.utils import timezone
from users.models import CustomUser

class Job(models.Model):
    """Model for job postings"""
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=[
        ('FULL_TIME', 'Integral'),
        ('PART_TIME', 'Parcial'),
        ('CONTRACT', 'Contrato'),
        ('INTERNSHIP', 'Estágio'),
    ])
    
    recruiter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posted_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    class Meta:
        ordering = ['-created_at']


class Application(models.Model):
    """Model for job applications"""
    class Status(models.TextChoices):
        APPLIED = 'APPLIED', 'Candidatado'
        REVIEWING = 'REVIEWING', 'Em análise'
        SHORTLISTED = 'SHORTLISTED', 'Pré-selecionado'
        REJECTED = 'REJECTED', 'Rejeitado'
        HIRED = 'HIRED', 'Contratado'

    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recruiter_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.candidate.username} application for {self.job.title}"
    
    class Meta:
        # Ensure a candidate can only apply once for a specific job
        unique_together = ('job', 'candidate')
        ordering = ['-applied_at']
