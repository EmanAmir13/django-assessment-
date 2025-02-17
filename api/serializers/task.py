from rest_framework import serializers

from api.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'project', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Ensure that only members can update status.
        """
        request = self.context['request']
        user = request.user

        if request.method in ['PATCH', 'PUT']:  # Update requests
            if user.role == 'member' and len(data) > 1:
                raise serializers.ValidationError("Members can only update the task status.")
        return data
