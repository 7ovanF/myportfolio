from django.urls import path

from .views import landing_page, projects, experience, create_project, \
    get_projects_json, delete_project, create_experience, get_experiences_json, delete_experience

app_name = "main"

urlpatterns = [
    path('', landing_page, name="landing_page"),

    path('projects', projects, name="projects"),
    path('projects/add', create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),

    path('experience', experience, name="experience"),
    path('experience/add', create_experience, name="create_experience"),
    path("api/experience/", get_experiences_json, name="get_experiences_json"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
]
