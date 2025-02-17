from django.urls import path

from api.views.authentications import RegisterView, LoginView
from api.views.projects import ProjectListCreateView, ProjectDetailView
from api.views.tasks import TaskListCreateView, TaskDetailView

urlpatterns = [
    # authentications
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # projects
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),

    # tasks
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
