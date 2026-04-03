from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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

    return Response({
        "task": task.title,
        "completion_report": task.completion_report,
        "worked_hours": task.worked_hours
    })

@login_required
def dashboard(request):

    if request.user.role == 'superadmin':
        users = User.objects.all()
        tasks = Task.objects.all()

        return render(request, 'dashboard.html', {
            'users': users,
            'tasks': tasks,
            'role': 'superadmin'
        })

    elif request.user.role == 'admin':
        tasks = Task.objects.filter(assigned_to=request.user)

        return render(request, 'dashboard.html', {
            'tasks': tasks,
            'role': 'admin'
        })

    else:
        # normal user (optional)
        tasks = Task.objects.filter(assigned_to=request.user)

        return render(request, 'dashboard.html', {
            'tasks': tasks,
            'role': 'user'
        })