from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Profile management
    path('profile/', views.profile, name='profile'),
    
    # Admin views
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-management/', views.UserManagementView.as_view(), name='user_management'),
    path('toggle-user-active/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
]
