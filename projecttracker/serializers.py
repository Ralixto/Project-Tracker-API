from .models import User, Project, Task, TaskAssignment
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Project
        fields = ['id', 'name', 'owner', 'members', 'description', 'status', 'budget', 'risk_level', 'priority', 'start_date', 'end_date', 'updated_at', 'created_at']
        read_only_fields = ['owner', 'updated_at', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Task
        fields = ['title', 'project', 'description', 'status', 'risk_level', 'assigned_to', 'start_date', 'due_date', 'estimated_hours', 'actual_hours', 'updated_at', 'created_at']
        read_only_fields = ['created_at', 'updated_at']

class TaskAssignmentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TaskAssignment
        fields = ['task', 'user', 'assigned_by', 'assigned_at']
        read_only_fields = ['assigned_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']