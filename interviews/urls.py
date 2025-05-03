from django.urls import path
from . import views

urlpatterns = [
    path('schedule/<int:application_id>/', views.schedule_interview, name='schedule_interview'),
    path('<int:interview_id>/', views.interview_detail, name='interview_detail'),
    path('<int:pk>/update/', views.InterviewUpdateView.as_view(), name='interview_update'),
    path('<int:interview_id>/cancel/', views.cancel_interview, name='cancel_interview'),
    path('my-interviews/', views.my_interviews, name='my_interviews'),
    path('<int:interview_id>/feedback/', views.add_feedback, name='add_feedback'),
]
