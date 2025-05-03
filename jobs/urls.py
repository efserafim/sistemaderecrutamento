from django.urls import path
from . import views

urlpatterns = [
    # Job views
    path('', views.JobListView.as_view(), name='job_list'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('create/', views.JobCreateView.as_view(), name='job_create'),
    path('<int:pk>/update/', views.JobUpdateView.as_view(), name='job_update'),
    path('<int:job_id>/toggle-status/', views.toggle_job_status, name='toggle_job_status'),
    path('my-jobs/', views.my_posted_jobs, name='my_posted_jobs'),
    
    # Application views
    path('<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('<int:job_id>/applications/', views.view_applications, name='view_applications'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
]
