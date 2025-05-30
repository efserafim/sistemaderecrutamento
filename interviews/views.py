from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone

from .models import Interview
from jobs.models import Application
from .forms import InterviewForm

@login_required
def schedule_interview(request, application_id):
    """
    Allow recruiters to schedule an interview for a selected application
    """
    application = get_object_or_404(Application, pk=application_id)
    

    if request.user != application.job.recruiter and not request.user.is_admin():
        return HttpResponseForbidden("Você não tem permissão para agendar entrevistas para esta aplicação.")
    
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            
     
            if application.status == Application.Status.APPLIED:
                application.status = Application.Status.REVIEWING
                application.save()
            
            messages.success(request, "Entrevista agendada com sucesso!")
            return redirect('application_detail', application_id=application.id)
    else:

        form = InterviewForm(initial={
            'date_time': timezone.now() + timezone.timedelta(days=3, hours=9),
            'duration_minutes': 45
        })
    
    return render(request, 'interviews/interview_form.html', {
        'form': form,
        'application': application,
        'title': f'Programar Entrevista com o  {application.candidate.get_full_name() or application.candidate.username}'
    })

@login_required
def interview_detail(request, interview_id):
    """
    Show interview details with option to update status/feedback by the recruiter
    """
    interview = get_object_or_404(Interview, pk=interview_id)
    
    
    is_recruiter = request.user == interview.recruiter
    is_candidate = request.user == interview.candidate
    is_admin = request.user.is_admin()
    
    if not (is_recruiter or is_candidate or is_admin):
        return HttpResponseForbidden("You don't have permission to view this interview.")
    
    if request.method == 'POST' and (is_recruiter or is_admin):
        form = InterviewForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, "Interview updated successfully!")
            return redirect('interview_detail', interview_id=interview.id)
    else:
        form = InterviewForm(instance=interview) if (is_recruiter or is_admin) else None
    
    context = {
        'interview': interview,
        'form': form,
        'is_recruiter': is_recruiter or is_admin,
        'is_candidate': is_candidate,
        'application': interview.application
    }
    
    return render(request, 'interviews/interview_detail.html', context)

class InterviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow recruiters to update interview details
    """
    model = Interview
    form_class = InterviewForm
    template_name = 'interviews/interview_form.html'
    
    def get_success_url(self):
        return reverse('interview_detail', kwargs={'interview_id': self.object.id})
    
    def test_func(self):
        interview = self.get_object()
        return self.request.user == interview.recruiter or self.request.user.is_admin()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Interview'
        context['application'] = self.object.application
        return context

@login_required
def cancel_interview(request, interview_id):
    """
    Allow recruiters to cancel an interview
    """
    interview = get_object_or_404(Interview, pk=interview_id)
    

    if request.user != interview.recruiter and not request.user.is_admin():
        return HttpResponseForbidden("You don't have permission to cancel this interview.")
    
    if request.method == 'POST':
        interview.status = Interview.InterviewStatus.CANCELED
        interview.save()
        messages.success(request, "Interview has been canceled.")
        return redirect('my_interviews')
    
    return render(request, 'interviews/confirm_cancel.html', {
        'interview': interview
    })

@login_required
def my_interviews(request):
    """
    Show upcoming interviews for either candidate or recruiter
    """
    now = timezone.now()
    
    if request.user.is_candidate():
        
        interviews = Interview.objects.filter(
            application__candidate=request.user,
            date_time__gte=now
        ).select_related('application__job', 'application__candidate')
        
        title = 'Minhas próximas entrevistas'
        
    elif request.user.is_recruiter():
        
        interviews = Interview.objects.filter(
            application__job__recruiter=request.user,
            date_time__gte=now
        ).select_related('application__job', 'application__candidate')
        
        title = 'Próximas entrevistas que agendei'
        
    else:
        
        interviews = Interview.objects.filter(
            date_time__gte=now
        ).select_related('application__job', 'application__candidate')
        
        title = 'Todas as próximas entrevistas'
    

    past_interviews = Interview.objects.filter(
        date_time__lt=now
    )
    
    if request.user.is_candidate():
        past_interviews = past_interviews.filter(application__candidate=request.user)
    elif request.user.is_recruiter():
        past_interviews = past_interviews.filter(application__job__recruiter=request.user)
    
    past_interviews = past_interviews.select_related(
        'application__job', 'application__candidate'
    ).order_by('-date_time')[:10]  
    
    return render(request, 'interviews/interview_list.html', {
        'interviews': interviews,
        'past_interviews': past_interviews,
        'title': title,
        'now': now
    })

@login_required
def add_feedback(request, interview_id):
    """
    Allow recruiters to add feedback after an interview
    """
    interview = get_object_or_404(Interview, pk=interview_id)
    
   
    if request.user != interview.recruiter and not request.user.is_admin():
        return HttpResponseForbidden("Você não tem permissão para adicionar feedback para esta entrevista.")
    
    
    if not interview.is_past:
        messages.error(request, "Você só pode adicionar feedback para entrevistas que já ocorreram.")
        return redirect('interview_detail', interview_id=interview.id)
    
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        new_status = request.POST.get('status')
        
        if feedback:
            interview.feedback = feedback
            
        if new_status:
            interview.status = new_status
            
        interview.save()
        
        
        if new_status == Interview.InterviewStatus.COMPLETED:
            application = interview.application
            if application.status == Application.Status.REVIEWING:
                application.status = Application.Status.SHORTLISTED
                application.save()
        
        messages.success(request, "Feedback adicionado com sucesso!")
        return redirect('interview_detail', interview_id=interview.id)
    
    return render(request, 'interviews/add_feedback.html', {
        'interview': interview
    })
