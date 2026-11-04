from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import ProjectViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project') # project-list, project-create...

urlpatterns = [
    path('/', include(router.urls))
]
