from django.shortcuts import get_object_or_404, render, redirect
from django.core import serializers
from django.http import HttpResponse
from django.contrib import messages

from .models import Project, Experience
from .forms import ProjectForm

# fix from https://www.perplexity.ai/search/5b78a4ab-e9fe-454e-ba49-ff7122f099a2
base_context = {
    "full_name": "Jovan Finesta",
    "display_name": "7ovanF",
}

profile_context = {
    "npm": "2506599144",
    "study_program": "S1 Ilmu Komputer",
    "study_program_en": "Computer Science",
    "bio": [
        "A CS student at University of Indonesia.",
        "Interested in Linux systems, networking, security, a bit of self-hosting...",
        "I don't know what to self-host."
    ],
    "social_links": [
        {
            "label": "7ovanF",
            "icon_name": "logo-github",
            "url": "https://github.com/7ovanf"
        },
        {
            "label": "Jovan Finesta",
            "icon_name": "logo-linkedin",
            "url": "https://linkedin.com/in/jovan-finesta/"
        },
        {
            "label": "jovanfinesta [at] protonmail [dot] com",
            "icon_name": "mail-outline",
            "url": "mailto:jovanfinesta@protonmail.com"
        }
    ],
}

def landing_page(request):
    json_response = get_projects_json(request)
    projects = serializers.deserialize(
            "json",
            json_response.content.decode("utf-8"),
        )

    context = {
            "active_page": "landing_page",
            **base_context, **profile_context,
            "project_list": projects,
            "experience_list": Experience.objects.all(),
        }
    return render(request, "main/profile.html", context)

def projects(request):
    json_response = get_projects_json(request)
    projects = serializers.deserialize(
            "json",
            json_response.content.decode("utf-8"),
        )
    projects = [ project.object for project in projects ]

    context = {
            "active_page": "projects",
            **base_context,
            "project_list": projects,
        }
    return render(request, "main/projects.html", context)


def experience(request):
    context = {
            "active_page": "experience",
            **base_context,
            "experience_list": Experience.objects.all(),
        }
    return render(request, "main/experience.html", context)

# === APIs ===
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:projects")

    return redirect("main:projects")

# === Forms ===
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:projects")

    context = {
        **base_context,
        "form": form,
    }
    return render(request, "main/projects_form.html", context)