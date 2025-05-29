from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Job, Application
from .forms import JobForm, ApplicationForm, ApplicationStatusForm

class JobListView(ListView):
    """Visualizar para listar todos os empregos ativos para os candidatos navegarem"""
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)
        
   
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(company__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(requirements__icontains=search_query)
            )
        
        
        job_type = self.request.GET.get('job_type', '')
        if job_type:
            queryset = queryset.filter(job_type=job_type)
            
        location = self.request.GET.get('location', '')
        if location:
            queryset = queryset.filter(location__icontains=location)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['job_type_filter'] = self.request.GET.get('job_type', '')
        context['location_filter'] = self.request.GET.get('location', '')
        
        
        context['locations'] = Job.objects.filter(is_active=True).values_list('location', flat=True).distinct()
        
       
        if self.request.user.is_authenticated and self.request.user.is_candidate():
            applied_jobs = set(Application.objects.filter(
                candidate=self.request.user
            ).values_list('job_id', flat=True))
            context['applied_jobs'] = applied_jobs
            
        return context

class JobDetailView(DetailView):
    """View to show details of a specific job"""
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
      
        if user.is_authenticated and user.is_candidate():
            already_applied = Application.objects.filter(
                job=self.object, 
                candidate=user
            ).exists()
            context['already_applied'] = already_applied
            
            if not already_applied:
                context['application_form'] = ApplicationForm()
                
       
        if user.is_authenticated and (user.is_recruiter() or user.is_admin()):
            context['is_owner'] = self.object.recruiter == user
            context['application_count'] = Application.objects.filter(job=self.object).count()
            
        return context

@login_required
def apply_for_job(request, job_id):
    """Handle job application submission by candidates"""
    if not request.user.is_candidate():
        messages.error(request, "Somente candidatos podem se candidatar a vagas.")
        return redirect('job_list')
    
    job = get_object_or_404(Job, pk=job_id, is_active=True)
    
    
    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.info(request, "Você já se candidatou para esta vaga.")
        return redirect('job_detail', pk=job.pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save()
            messages.success(request, "Sua inscrição foi enviada com sucesso!")
            return redirect('job_detail', pk=job.pk)
    else:
        form = ApplicationForm()
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'application_form': form
    })

class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View for recruiters to create new job postings"""
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('my_posted_jobs')
    
    def form_valid(self, form):
        form.instance.recruiter = self.request.user
        messages.success(self.request, "Emprego postado com sucesso!")
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_recruiter()

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for recruiters to update their job postings"""
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    
    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, "Emprego atualizado com sucesso!")
        return super().form_valid(form)
    
    def test_func(self):
        job = self.get_object()
        return self.request.user == job.recruiter

@login_required
def toggle_job_status(request, job_id):
    """Allow recruiters to toggle a job's active status"""
    job = get_object_or_404(Job, pk=job_id)
    

    if request.user != job.recruiter and not request.user.is_admin():
        return HttpResponseForbidden("Você não tem permissão para modificar este trabalho.")
    
    job.is_active = not job.is_active
    job.save()
    
    status = "activated" if job.is_active else "deactivated"
    messages.success(request, f"Job '{job.title}' has been {status}.")
    
    return redirect('my_posted_jobs')

@login_required
def my_posted_jobs(request):
    """Show recruiters a list of jobs they have posted"""
    if not request.user.is_recruiter():
        messages.error(request, "Somente recrutadores podem visualizar vagas publicadas.")
        return redirect('home')
    
    jobs = Job.objects.filter(recruiter=request.user).order_by('-created_at')
    
  
    for job in jobs:
        job.application_count = job.applications.count()
    
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'is_my_jobs': True,
        'title': 'Meus empregos publicados'
    })

@login_required
def my_applications(request):
    """Show candidates a list of jobs they've applied to"""
    if not request.user.is_candidate():
        messages.error(request, "Somente os candidatos podem visualizar as inscrições.")
        return redirect('home')
    
    applications = Application.objects.filter(candidate=request.user).select_related('job')
    
    return render(request, 'jobs/application_list.html', {
        'applications': applications,
        'title': 'My Applications'
    })

@login_required
def view_applications(request, job_id):
    """Let recruiters view applications for a specific job"""
    job = get_object_or_404(Job, pk=job_id)
    
  
    if request.user != job.recruiter and not request.user.is_admin():
        return HttpResponseForbidden("Você não tem permissão para visualizar candidaturas para esta vaga.")
    
    applications = Application.objects.filter(job=job).select_related('candidate')
    
    return render(request, 'jobs/application_list.html', {
        'applications': applications,
        'job': job,
        'title': f'Applications for {job.title}'
    })

@login_required
def application_detail(request, application_id):
    """Show detailed view of an application with option to update status"""
    application = get_object_or_404(Application, pk=application_id)
    

    is_recruiter = request.user == application.job.recruiter
    is_candidate = request.user == application.candidate
    is_admin = request.user.is_admin()
    
    if not (is_recruiter or is_candidate or is_admin):
        return HttpResponseForbidden("You don't have permission to view this application.")
    
    if request.method == 'POST' and (is_recruiter or is_admin):
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Status da aplicação atualizado com sucesso!")
            return redirect('application_detail', application_id=application.id)
    else:
        form = ApplicationStatusForm(instance=application) if (is_recruiter or is_admin) else None
    
    context = {
        'application': application,
        'form': form,
        'is_recruiter': is_recruiter or is_admin,
        'is_candidate': is_candidate
    }
    
    return render(request, 'jobs/application_detail.html', context)
