from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import User

from .models import Task
from .serializers import TaskSerializer



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, id):
    task = get_object_or_404(Task, id=id, assigned_to=request.user)

    if request.data.get("status") == "completed":
        if not request.data.get("completion_report") or not request.data.get("worked_hours"):
            return Response(
                {"error": "Completion report and worked hours required"},
                status=400
            )

    serializer = TaskSerializer(task, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_report(request, id):

    if request.user.role not in ['admin', 'superadmin']:
        return Response({"error": "Unauthorized"}, status=403)

    task = get_object_or_404(Task, id=id, status='completed')

    if request.user.role == 'admin' and task.assigned_to.assigned_admin != request.user:
        return Response({"error": "Unauthorized"}, status=403)

    return Response({
        "task": task.title,
        "completion_report": task.completion_report,
        "worked_hours": task.worked_hours
    })

@login_required
def dashboard(request):
    if request.user.role == 'superadmin':
        users = User.objects.all()
        tasks = Task.objects.all().order_by('-id')
        return render(request, 'dashboard.html', {
            'users': users,
            'tasks': tasks,
            'role': 'superadmin'
        })
    elif request.user.role == 'admin':
        managed_users = User.objects.filter(assigned_admin=request.user)
        tasks = Task.objects.filter(assigned_to__in=managed_users).order_by('-id')
        return render(request, 'dashboard.html', {
            'tasks': tasks,
            'role': 'admin'
        })
    else:
        tasks = Task.objects.filter(assigned_to=request.user).order_by('-id')
        return render(request, 'dashboard.html', {
            'tasks': tasks,
            'role': 'user'
        })

@login_required
def task_list(request):
    if request.user.role == 'superadmin':
        tasks = Task.objects.all().order_by('-due_date')
    elif request.user.role == 'admin':
        managed_users = User.objects.filter(assigned_admin=request.user)
        tasks = Task.objects.filter(assigned_to__in=managed_users).order_by('-due_date')
    else:
        return redirect('dashboard')
    
    return render(request, 'task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.user.role not in ['admin', 'superadmin']:
        return redirect('dashboard')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')
        
        if request.user.role == 'admin':
            managed_user = User.objects.filter(id=assigned_to_id, assigned_admin=request.user).first()
            if not managed_user:
                messages.error(request, "You can only assign tasks to users managed by you.")
                return redirect('task_create')
                
        task = Task.objects.create(
            title=title,
            description=description,
            assigned_to_id=assigned_to_id,
            due_date=due_date,
            status=status
        )
        task.save()
        messages.success(request, 'Task created successfully.')
        return redirect('task_list')
        
    if request.user.role == 'superadmin':
        users = User.objects.all()
    else:
        users = User.objects.filter(assigned_admin=request.user)
        
    return render(request, 'task_form.html', {'users': users})

@login_required
def task_update(request, id):
    if request.user.role not in ['admin', 'superadmin']:
        return redirect('dashboard')
        
    task = get_object_or_404(Task, id=id)
    
    if request.user.role == 'admin' and task.assigned_to.assigned_admin != request.user:
        return redirect('dashboard')
        
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date')
        task.status = request.POST.get('status')
        new_assigned_to = request.POST.get('assigned_to')
        
        if request.user.role == 'admin':
            managed_user = User.objects.filter(id=new_assigned_to, assigned_admin=request.user).first()
            if not managed_user:
                messages.error(request, "You can only assign tasks to users managed by you.")
                return redirect('task_update', id=task.id)
                
        task.assigned_to_id = new_assigned_to
        
        if task.status == 'completed':
            task.completion_report = request.POST.get('completion_report', '')
            worked_hours = request.POST.get('worked_hours')
            if worked_hours:
                task.worked_hours = float(worked_hours)
                
        task.save()
        messages.success(request, 'Task updated successfully.')
        return redirect('task_list')
        
    if request.user.role == 'superadmin':
        users = User.objects.all()
    else:
        users = User.objects.filter(assigned_admin=request.user)
        
    return render(request, 'task_form.html', {'object': task, 'users': users})

@login_required
def task_delete(request, id):
    if request.user.role not in ['admin', 'superadmin']:
        return redirect('dashboard')
        
    task = get_object_or_404(Task, id=id)
    if request.user.role == 'admin' and task.assigned_to.assigned_admin != request.user:
        return redirect('dashboard')
        
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')
        
    return redirect('task_list')

@login_required
def task_report_view(request, id):
    if request.user.role not in ['admin', 'superadmin']:
        return redirect('dashboard')
        
    task = get_object_or_404(Task, id=id, status='completed')
    if request.user.role == 'admin' and task.assigned_to.assigned_admin != request.user:
        return redirect('dashboard')
        
    return render(request, 'task_report.html', {'task': task})