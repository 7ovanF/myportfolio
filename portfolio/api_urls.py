from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import ProjectViewSet, experience_list, experience_detail, experience_toggle_star

app_name = 'api'

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project') # project-list, project-create...

urlpatterns = [
    path('/', include(router.urls)),
    path('/experience', experience_list, name="experience-list"),
    path('/experience/<uuid:experience_id>', experience_detail, name="experience-detail"),
    path('/experience/<uuid:experience_id>/toggle_star', experience_toggle_star, name="experience-toggle_star"),
]
