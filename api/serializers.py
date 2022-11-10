from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'content', 'completed', 'created_at']
        # I want to get the ID and date for future filtering so, i want to see it but no edit it.
        read_only_fields = ['id', 'created_at']
