from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views.authentications import RegisterView, LoginView
from api.views.projects import ProjectListCreateView, ProjectDetailView
from api.views.tasks import TaskListCreateView, TaskDetailView
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Task Management API",
        default_version='v1',
        description="API for managing tasks within a project",
        contact=openapi.Contact(email="eman13.amir@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    # ReDoc UI (alternative to Swagger UI)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]
