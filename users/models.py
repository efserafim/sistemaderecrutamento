from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Custom user model with role-based access control for the recruitment system.
    Roles can be 'candidate', 'recruiter', or 'admin'.
    """
    class Role(models.TextChoices):
        CANDIDATE = 'CANDIDATE', _('Candidate')
        RECRUITER = 'RECRUITER', _('Recruiter')
        ADMIN = 'ADMIN', _('Administrator')
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CANDIDATE,
        help_text=_('Determines the user type and permissions')
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    def is_candidate(self):
        return self.role == self.Role.CANDIDATE
    
    def is_recruiter(self):
        return self.role == self.Role.RECRUITER
    
    def is_admin(self):
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class CandidateProfile(models.Model):
    """Additional information related to candidates"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidate_profile')
    resume = models.TextField(blank=True, null=True, help_text=_('Candidate resume text'))
    skills = models.TextField(blank=True, null=True, help_text=_('Candidate skills (comma separated)'))
    experience = models.IntegerField(default=0, help_text=_('Years of experience'))
    education = models.TextField(blank=True, null=True, help_text=_('Education history'))

    def __str__(self):
        return f"Profile for {self.user.username}"


class RecruiterProfile(models.Model):
    """Additional information related to recruiters"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
    company = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Profile for {self.user.username} at {self.company}"
