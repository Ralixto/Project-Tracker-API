from .models import User, Project, Task, TaskAssignment
from .serializers import ProjectSerializer, TaskAssignmentSerializer, TaskSerializer, RegisterSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .paginations import CustomPageNumberPagination
from .permissions import IsAssignedOrReadOnly
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Count, Q

# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAssignedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def health(self, request):
        today = timezone.now().date()
        
        projects = Project.objects.annotate(
            total_tasks=Count('tasks'),
            completed_tasks=Count('tasks', filter=Q(tasks__status='COMP')),
            overdue_tasks=Count('tasks', filter=Q(tasks__due_date__lt=today) & ~Q(tasks__status='COMP')),
        ).select_related('owner')

        data = []
        for project in projects:
            completion_rate = (
                (project.completed_tasks / project.total_tasks * 100)
                if project.total_tasks > 0 else 0
            )
            is_overdue = today > project.end_date

            data.append({
                'id': project.id,
                'name': project.name,
                'status': project.status,
                'owner': project.owner.username,
                'total_tasks': project.total_tasks,
                'completed_tasks': project.completed_tasks,
                'overdue_tasks': project.overdue_tasks,
                'completion_rate': round(completion_rate, 1),
                'is_overdue': is_overdue,
                'end_date': project.end_date,
                'risk_level': project.risk_level,
            })

        return Response(data)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAssignedOrReadOnly, IsAuthenticatedOrReadOnly]

class TaskAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer
    permission_classes = [IsAssignedOrReadOnly, IsAuthenticated]

class RegisterView(APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)