from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage_allocations/', views.manage_allocations, name='manage_allocations'),
    path('project_reports/', views.project_reports, name='project_reports'),
    path('resource_reports/', views.resource_reports, name='resource_reports'),
    path('add_project/', views.add_project, name='add_project'),
    path('add_resource/', views.add_resource, name='add_resource'),
    path('view_allocation/<int:resource_id>/', views.view_allocation, name='view_allocation'),
    path('project_allocation/<int:project_id>/', views.view_project_allocation, name='view_project_allocation'),
]
