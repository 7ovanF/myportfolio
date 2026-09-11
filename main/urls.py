from django.urls import path

from .views import landing_page, projects, experience

app_name = "main"

urlpatterns = [
    path('', landing_page, name="landing_page"),
    path('projects', projects, name="projects"),
    path('experience', experience, name="experience"),
]
