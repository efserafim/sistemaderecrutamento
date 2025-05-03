from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    """Form for creating and updating job postings"""
    class Meta:
        model = Job
        fields = [
            'title', 'company', 'location', 'description', 
            'requirements', 'salary_range', 'job_type', 'deadline', 'is_active'
        ]
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 6}),
            'requirements': forms.Textarea(attrs={'rows': 6}),
        }

class ApplicationForm(forms.ModelForm):
    """Form for candidates to apply for jobs"""
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 6, 
                'placeholder': 'Explain why you are a good fit for this position...'
            }),
        }

class ApplicationStatusForm(forms.ModelForm):
    """Form for recruiters to update application status and add notes"""
    class Meta:
        model = Application
        fields = ['status', 'recruiter_notes']
        widgets = {
            'recruiter_notes': forms.Textarea(attrs={'rows': 4}),
        }

class JobSearchForm(forms.Form):
    """Form for filtering and searching jobs"""
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search jobs...',
        'class': 'form-control'
    }))
    job_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + list(Job.job_type.field.choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Location',
        'class': 'form-control'
    }))
