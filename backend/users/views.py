from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# --- User Management Views (SuperAdmin only) ---
@login_required
def user_list(request):
    if request.user.role != 'superadmin':
        return redirect('dashboard')
    users_list = User.objects.all().order_by('-id')
    return render(request, 'user_list.html', {'users_list': users_list})

@login_required
def user_create(request):
    if request.user.role != 'superadmin':
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        assigned_admin_id = request.POST.get('assigned_admin')

        user = User(username=username, role=role)
        if password:
            user.set_password(password)
        if assigned_admin_id:
            user.assigned_admin_id = assigned_admin_id
        user.save()
        messages.success(request, 'User created successfully.')
        return redirect('user_list')
        
    admins = User.objects.filter(role='admin')
    return render(request, 'user_form.html', {'admins': admins})

@login_required
def user_update(request, id):
    if request.user.role != 'superadmin':
        return redirect('dashboard')
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.role = request.POST.get('role')
        password = request.POST.get('password')
        assigned_admin_id = request.POST.get('assigned_admin')
        
        if password:
            user.set_password(password)
        
        user.assigned_admin_id = assigned_admin_id if assigned_admin_id else None
        user.save()
        messages.success(request, 'User updated successfully.')
        return redirect('user_list')
        
    admins = User.objects.filter(role='admin')
    return render(request, 'user_form.html', {'object': user, 'admins': admins})

@login_required
def user_delete(request, id):
    if request.user.role != 'superadmin':
        return redirect('dashboard')
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'object': user})