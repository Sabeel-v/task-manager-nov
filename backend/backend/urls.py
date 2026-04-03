"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import (
    login_view, logout_view, 
    user_list, user_create, user_update, user_delete
)
from tasks.views import (
    dashboard, 
    task_list, task_create, task_update, task_delete, task_report_view
)

urlpatterns = [
    # Auth Web pages
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # User Management Web pages
    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/<int:id>/edit/', user_update, name='user_update'),
    path('users/<int:id>/delete/', user_delete, name='user_delete'),

    # Task Management Web pages
    path('manage-tasks/', task_list, name='task_list'),
    path('manage-tasks/create/', task_create, name='task_create'),
    path('manage-tasks/<int:id>/edit/', task_update, name='task_update'),
    path('manage-tasks/<int:id>/delete/', task_delete, name='task_delete'),
    path('manage-tasks/<int:id>/report/', task_report_view, name='task_report_view'),

    # Admin
    path('admin/', admin.site.urls),

    # APIs
    path('api/', include('tasks.urls')),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]