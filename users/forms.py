from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, CandidateProfile, RecruiterProfile

class UserRegisterForm(UserCreationForm):
    """Form for user registration with role selection"""
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[(CustomUser.Role.CANDIDATE, 'Candidate'), (CustomUser.Role.RECRUITER, 'Recruiter')],
        widget=forms.RadioSelect,
        initial=CustomUser.Role.CANDIDATE
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

class UserUpdateForm(forms.ModelForm):
    """Form for updating basic user information"""
    email = forms.EmailField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class CandidateProfileForm(forms.ModelForm):
    """Form for updating candidate-specific profile information"""
    class Meta:
        model = CandidateProfile
        fields = ['resume', 'skills', 'experience', 'education']
        widgets = {
            'resume': forms.Textarea(attrs={'rows': 8}),
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g., Python, Django, HTML/CSS, JavaScript'}),
            'education': forms.Textarea(attrs={'rows': 3}),
        }

class RecruiterProfileForm(forms.ModelForm):
    """Form for updating recruiter-specific profile information"""
    class Meta:
        model = RecruiterProfile
        fields = ['company', 'position', 'department']
