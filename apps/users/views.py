# apps/users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from .models import CustomUser
from .forms import CustomLoginForm, CustomUserForm


# Utility function for role-based checks
# apps/users/views.py
def is_admin(user):
    return user.is_authenticated and (user.role == 'Admin' or user.is_superuser)



def index(request):
    """ User home page view. """
    users = CustomUser.objects.all()
    return render(request, 'users/index.html', {'title': 'Users', 'users': users})


@login_required
def profile(request):
    """ User profile view for logged-in users. """
    return render(request, 'users/profile.html', {'title': 'User Profile', 'user': request.user})


@login_required
def custom_logout(request):
    """ Logs out the user and redirects to the login page. """
    logout(request)
    return redirect('login')


@user_passes_test(is_admin)
def manage_users(request):
    """ View to manage all users. Only accessible to Admin users. """
    users = CustomUser.objects.all()
    return render(request, 'users/manage_users.html', {'users': users, 'title': 'Manage Users'})


@user_passes_test(is_admin)
def add_user(request):
    """ Add a new user. Accessible only to Admins. """
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()  # Password hashing is handled in the form
            return redirect('manage-users')
    else:
        form = CustomUserForm()
    return render(request, 'users/add_user.html', {'form': form, 'title': 'Add User'})


@user_passes_test(is_admin)
def edit_user(request, user_id):
    """ Edit an existing user. Accessible only to Admins. """
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Password hashing is handled in the form
            return redirect('manage-users')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'title': 'Edit User'})


@user_passes_test(is_admin)
def delete_user(request, user_id):
    """ Delete a user. Accessible only to Admins. """
    user = get_object_or_404(CustomUser, pk=user_id)
    user.delete()
    return redirect('manage-users')
