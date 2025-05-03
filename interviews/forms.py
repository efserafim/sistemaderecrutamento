from django import forms
from .models import Interview
from django.utils import timezone

class InterviewForm(forms.ModelForm):
    """Form for scheduling and updating interviews"""
    class Meta:
        model = Interview
        fields = [
            'interview_type', 'date_time', 'duration_minutes', 
            'location', 'status', 'notes'
        ]
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_date_time(self):
        """Ensure interview is scheduled in the future"""
        date_time = self.cleaned_data.get('date_time')
        now = timezone.now()
        
        if date_time and date_time < now:
            raise forms.ValidationError("You cannot schedule an interview in the past.")
        
        return date_time
