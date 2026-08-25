from rest_framework import routers
from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('api/register/', views.RegisterView.as_view(), name='api-register'),
    path('api/token/', TokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

router = routers.DefaultRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'task', views.TaskViewSet)
router.register(r'task-assignment', views.TaskAssignmentViewSet)

urlpatterns += router.urls