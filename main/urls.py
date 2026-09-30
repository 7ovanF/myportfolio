from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path('', views.landing_page, name="landing_page"),

    path('projects', views.projects, name="projects"),
    path('projects/add', views.create_project, name="create_project"),
    path('projects/add-ajax', views.create_project_ajax, name="create_project_ajax"),
    path('projects/<uuid:project_id>/edit', views.update_project, name="update_project"),
    path("projects/<uuid:project_id>/delete", views.delete_project, name="delete_project"),
    path('projects/<uuid:project_id>/star', views.toggle_project_star, name="toggle_project_star"),
    path("api/projects/", views.get_projects_json, name="get_projects_json"),

    path('experience', views.experience, name="experience"),
    path('experience/add', views.create_experience, name="create_experience"),
    path('experience/<uuid:experience_id>/star', views.toggle_experience_star, name="toggle_experience_star"),
    path('experience/<uuid:experience_id>/edit', views.update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete", views.delete_experience, name="delete_experience"),
    path("api/experience/", views.get_experiences_json, name="get_experiences_json"),
]
