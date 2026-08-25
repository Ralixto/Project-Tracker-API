from django.contrib import admin
from .models import User, Project, Task, TaskAssignment
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskAssignment)