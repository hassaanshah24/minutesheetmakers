# apps/users/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

urlpatterns = [
    path('', views.index, name='users-home'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        authentication_form=CustomLoginForm
    ), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('manage_users/', views.manage_users, name='manage-users'),
    path('add_user/', views.add_user, name='add-user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit-user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete-user'),
]
