from rest_framework import generics, permissions, response, status

from api.models import Project
from api.permissions import IsAdmin
from api.serializers.project import ProjectSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    """List all projects or create a new one (Admins only)."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAdmin]  # Only Admins can create
        return self.create(request, *args, **kwargs)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a project. Only Admins can delete."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAdmin]  # Only Admins can delete
        project = self.get_object()
        response_message = {"message": f"Project '{project.title}' has been deleted successfully."}
        return self.destroy(request, *args, **kwargs, response_message=response_message)

    def put(self, request, *args, **kwargs):
        """Override update to return a success message."""
        project = self.get_object()
        self.update(request, *args, **kwargs)
        return response.Response(
            {"message": f"Project '{project.title}' has been updated successfully."},
            status=status.HTTP_200_OK
        )
