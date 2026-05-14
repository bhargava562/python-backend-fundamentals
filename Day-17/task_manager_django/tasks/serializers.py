from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=1, max_length=200)
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "is_completed"]
