from rest_framework import serializers

from api.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'creator', 'created_at', 'updated_at']
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Ensure only admins can create projects.
        """
        user = self.context['request'].user
        if user.role != 'admin':
            raise serializers.ValidationError("Only admins can create or update projects.")
        return data
