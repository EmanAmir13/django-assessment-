from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    custom permission to allow only admins to create or delete projects and tasks.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class CanUpdateTaskStatus(permissions.BasePermission):
    """
    custom permission to allow members to update only the status field of a task.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'member':
            return 'status' in request.data and len(request.data) == 1
        return False
