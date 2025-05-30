from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction

from .models import CustomUser, CandidateProfile, RecruiterProfile
from .forms import (
    UserRegisterForm,
    CandidateProfileForm,
    RecruiterProfileForm,
    UserUpdateForm
)

def register(request):
    """Handle user registration with profile creation based on the role"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
              
                user = form.save()
             
                if user.is_candidate():
                    CandidateProfile.objects.create(user=user)
                elif user.is_recruiter():
                    RecruiterProfile.objects.create(user=user)
                
             
                login(request, user)
                messages.success(request, 'Conta criada com sucesso! Complete seu perfil.')
                return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    """Handle profile updates for different user roles"""
    user = request.user
    profile_form = None
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        
       
        if user.is_candidate():
            profile, created = CandidateProfile.objects.get_or_create(user=user)
            profile_form = CandidateProfileForm(request.POST, instance=profile)
        elif user.is_recruiter():
            profile, created = RecruiterProfile.objects.get_or_create(user=user)
            profile_form = RecruiterProfileForm(request.POST, instance=profile)
        
       
        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Seu perfil foi atualizado!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        
        if user.is_candidate():
            profile, created = CandidateProfile.objects.get_or_create(user=user)
            profile_form = CandidateProfileForm(instance=profile)
        elif user.is_recruiter():
            profile, created = RecruiterProfile.objects.get_or_create(user=user)
            profile_form = RecruiterProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)

@method_decorator(login_required, name='dispatch')
class UserManagementView(UserPassesTestMixin, ListView):
    """View for administrators to manage all users in the system"""
    model = CustomUser
    template_name = 'users/user_management.html'
    context_object_name = 'users'
    
    def test_func(self):
        return self.request.user.is_admin()

@login_required
def admin_dashboard(request):
    """Dashboard for admin users with system statistics"""
    if not request.user.is_admin():
        messages.error(request, "Você não tem permissão para visualizar esta página")
        return redirect('home')
    
    
    total_users = CustomUser.objects.count()
    candidate_count = CustomUser.objects.filter(role=CustomUser.Role.CANDIDATE).count()
    recruiter_count = CustomUser.objects.filter(role=CustomUser.Role.RECRUITER).count()
    admin_count = CustomUser.objects.filter(role=CustomUser.Role.ADMIN).count()
    
    context = {
        'total_users': total_users,
        'candidate_count': candidate_count,
        'recruiter_count': recruiter_count,
        'admin_count': admin_count,
    }
    return render(request, 'users/admin_dashboard.html', context)

@login_required
def toggle_user_active(request, user_id):
    """Toggle a user's active status (for admin use)"""
    if not request.user.is_admin():
        messages.error(request, "Você não tem permissão para executar esta ação")
        return redirect('home')
    
    user = get_object_or_404(CustomUser, id=user_id)
    
   
    if user == request.user:
        messages.error(request, "Você não pode desativar sua própria conta")
        return redirect('user_management')
    
    user.is_active = not user.is_active
    user.save()
    
    status = "ativado" if user.is_active else "desativado"
    messages.success(request, f"User {user.username} has been {status}")
    return redirect('user_management')
