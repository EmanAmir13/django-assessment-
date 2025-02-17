from rest_framework import generics, permissions, response, status
from api.models import Task
from api.permissions import IsAdmin, CanUpdateTaskStatus
from api.serializers.task import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    """List all tasks or create a new one (Admins only)."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAdmin]  # Only Admins can create tasks
        response_data = self.create(request, *args, **kwargs)
        return response.Response(
            {"message": "Task created successfully", "task": response_data.data},
            status=status.HTTP_201_CREATED
        )

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a task. Only Admins can delete, Members can update status."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """Only Admins can delete tasks."""
        self.permission_classes = [IsAdmin]
        task = self.get_object()
        response_data = super().destroy(request, *args, **kwargs)
        return response.Response(
            {"message": f"Task '{task.title}' has been deleted successfully."},
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        """Members can update task status."""
        self.permission_classes = [CanUpdateTaskStatus]
        response_data = super().partial_update(request, *args, **kwargs)
        task = self.get_object()
        return response.Response(
            {"message": f"Task '{task.title}' status updated successfully.", "task": response_data.data},
            status=status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        """Members can update task status."""
        self.permission_classes = [CanUpdateTaskStatus]
        response_data = super().update(request, *args, **kwargs)
        task = self.get_object()
        return response.Response(
            {"message": f"Task '{task.title}' has been updated successfully.", "task": response_data.data},
            status=status.HTTP_200_OK
        )
