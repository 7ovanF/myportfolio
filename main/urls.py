from django.urls import path

from .views import landing_page, projects

app_name = "main"

urlpatterns = [
    path('', landing_page, name="landing_page"),
    path('projects', projects, name="projects"),
]
