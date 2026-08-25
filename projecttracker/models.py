from django.db import models
from django.contrib.auth.models import AbstractUser

class PriorityLevels(models.TextChoices):
    LOW = 'L', 'Low'
    MEDIUM = 'M', 'Medium'
    HIGH = 'H', 'High'

class StatusChoices(models.TextChoices):
    PLANNING = 'PLAN', 'Planning'
    ACTIVE = 'ACT', 'Active / In Progress'
    COMPLETED = 'COMP', 'Completed'
    ON_HOLD = 'HOLD', 'On Hold'


class User(AbstractUser):
    pass

class Project(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    members = models.ManyToManyField(User, related_name='member_projects')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PLANNING)
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    risk_level = models.CharField(max_length=1, choices=PriorityLevels.choices, default=PriorityLevels.MEDIUM)
    priority = models.CharField(max_length=1, choices=PriorityLevels.choices, default=PriorityLevels.MEDIUM)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.name

class Task(models.Model):
    class TaskStatusChoices(models.TextChoices):
        BACKLOG = 'BGL', 'Backlog'
        PLANNING = 'PLAN', 'Planning'
        ACTIVE = 'ACT', 'Active / In Progress'
        COMPLETED = 'COMP', 'Completed'
        ON_HOLD = 'HOLD', 'On Hold'

    title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=TaskStatusChoices.choices, default=TaskStatusChoices.BACKLOG)
    risk_level = models.CharField(max_length=1, choices=PriorityLevels.choices, default=PriorityLevels.MEDIUM)
    assigned_to = models.ManyToManyField(User, through='TaskAssignment', through_fields=('task', 'user'), related_name='assigned_tasks', blank=True)    
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField()
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"[{self.project.name}] {self.title}"

class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_task_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks_created')
