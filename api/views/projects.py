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
        self.check_permissions(request)

        # mutable copy of request.data
        data = request.data.copy()
        data["creator"] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(
            {"message": f"Project '{serializer.data['title']}' has been created successfully."},
            status=status.HTTP_201_CREATED
        )


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a project. Only Admins can delete."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAdmin]  # Only Admins can delete
        self.check_permissions(request)  # Ensure permission is checked correctly

        project = self.get_object()
        super().delete(request, *args, **kwargs)  # Perform deletion

        return response.Response(
            {"message": f"Project '{project.title}' has been deleted successfully."},
            status=status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        """Override update to return a success message."""
        project = self.get_object()
        self.update(request, *args, **kwargs)
        return response.Response(
            {"message": f"Project '{project.title}' has been updated successfully."},
            status=status.HTTP_200_OK
        )
