from django.shortcuts import get_object_or_404, render, redirect
from django.core import serializers
from django.http import HttpResponse
from django.contrib import messages

from .models import Project, Experience
from .forms import ProjectForm, ExperienceForm

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
    json_projects = get_projects_json(request)
    projects = serializers.deserialize(
            "json",
            json_projects.content.decode("utf-8"),
        )
    projects = [ project.object for project in projects ]

    context = {
            "active_page": "landing_page",
            **base_context, **profile_context,
            "project_list": projects,
            "experience_list": Experience.objects.all(),
        }
    return render(request, "main/profile.html", context)

# ========
# PROJECTS 
# ========
def projects(request):
    json_projects = get_projects_json(request)
    projects = serializers.deserialize(
            "json",
            json_projects.content.decode("utf-8"),
        )
    projects = [ project.object for project in projects ]

    context = {
            "active_page": "projects",
            **base_context,
            "project_list": projects,
        }
    return render(request, "main/projects.html", context)

# APIs
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

# Forms 
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
    return render(request, "main/projects_add_form.html", context)

def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Successfully updated project!")
        return redirect("main:projects")

    context = {
        **base_context,
        "project": project,
        "form": form,
    }
    return render(request, "main/projects_edit_form.html", context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:projects")

    return redirect("main:projects")

# ==========
# EXPERIENCE
# ==========
# Refer to experience (plural) as experience*s* internally
def experience(request):
    json_experiences = get_experiences_json(request)
    experiences = serializers.deserialize(
            "json",
            json_experiences.content.decode("utf-8"),
        )
    experiences = [ experience.object for experience in experiences ]

    context = {
            "active_page": "experience",
            **base_context,
            "experience_list": experiences,
        }
    return render(request, "main/experience.html", context)

# APIs
def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

# Forms 
def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:experience")

    context = {
        **base_context,
        "form": form,
    }
    return render(request, "main/experience_add_form.html", context)

def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    form = ExperienceForm(request.POST or None, instance=experience)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Successfully updated experience!")
        return redirect("main:experience")

    context = {
        **base_context,
        "experience": experience,
        "form": form,
    }
    return render(request, "main/experience_edit_form.html", context)


def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:experience")

    return redirect("main:experience")
