from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from portfolio.decorators import superuser_required

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
    last_login = request.COOKIES.get('last_login', '')
    context = {
            "active_page": "landing_page",
            **base_context, **profile_context,
            "last_login": last_login,
            "project_form": ProjectForm(),
            "experience_form": ExperienceForm(),
        }
    return render(request, "main/profile.html", context)

# ========
# PROJECTS 
# ========
def projects(request):
    context = {
            "active_page": "projects",
            **base_context,
            "project_form": ProjectForm(),
        }
    return render(request, "main/projects.html", context)

# APIs
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    # prefetched as recommended by django ORM lens
    projects = Project.objects.prefetch_related("starred_by").prefetch_related("skills").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_by = project.starred_by.all()
        is_starred = request.user in starred_by if request.user.is_authenticated else False
        skill_titles = [skill.title for skill in project.skills.all()]
        starred_by_names = [user.username for user in starred_by]

        data.append({
            "id": str(project.pk),
            "title": project.title,
            "url": project.url,
            "thumbnail": project.thumbnail,
            "description": project.description,
            "skill_titles": skill_titles,
            "star_count": starred_by.count(),
            "is_starred": is_starred,
            "starred_by_names": starred_by_names,
        })
    response = {
        "data": data,
    }
    return JsonResponse(response, safe=False)

# Forms 
@login_required()
@permission_required('main.add_project', raise_exception=True)
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

@require_POST
def create_project_ajax(request):
    if not request.user.has_perm("main.add_project"):
        return JsonResponse(
            {"message": "Only the portfolio owner can add projects."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {"message": "Form invalid!"},
            status=400,
        )
    
    project = form.save()
    return JsonResponse(
        {"message": "Project added successfully.", "pk": str(project.id)},
        status=201,
    )

@login_required()
@permission_required('main.change_project', raise_exception=True)
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

@login_required()
@permission_required('main.delete_project', raise_exception=True)
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:projects")

    return redirect("main:projects")

@login_required()
def toggle_project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:projects")

# ==========
# EXPERIENCE
# ==========
# Refer to experience (plural) as experience*s* internally
def experience(request):
    context = {
            "active_page": "experience",
            **base_context,
            "experience_form": ExperienceForm(),
        }
    return render(request, "main/experience.html", context)

# APIs
def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related("starred_by").all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
    
    data = []
    for experience in experiences:
        is_starred = request.user in experience.starred_by.all()
        starred_by_names = [starrer.username for starrer in experience.starred_by.all()]
        data.append({
            "id": experience.id,
            "title": experience.title,
            "description": experience.description,
            "category": experience.category,
            "thumbnail": experience.thumbnail,
            "started_at": experience.started_at,
            "ended_at": experience.ended_at,
            "is_starred": is_starred,
            "starred_by_names": starred_by_names,
        })

    response = {
        "data": data
    }
    return JsonResponse(response, safe=False)

# Forms 
@login_required()
@permission_required('main.add_experience', raise_exception=True)
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

@require_POST
@login_required()
@permission_required("main.add_experience", raise_exception=True)
def create_experience_ajax(request):
    form = ExperienceForm(request.POST or None)

    if not form.is_valid():
        return JsonResponse(
            {"message": "Form invalid!"},
            status=400,
        )

    experience = form.save()
    return JsonResponse(
        {"message": "Experience added successfully.", "pk": str(experience.pk)},
        status=201,
    )

@login_required()
@permission_required('main.change_experience', raise_exception=True)
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


@login_required()
@permission_required('main.delete_experience', raise_exception=True)
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Successfully deleted experience.")
        return redirect("main:experience")

    return redirect("main:experience")

@require_POST
@login_required()
@permission_required('main.delete_experience', raise_exception=True)
def delete_experience_ajax(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    experience.delete()
    return JsonResponse(
        {"message": "Successfully deleted experience."},
        status=200
    )

@login_required()
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    
    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)
        
    return redirect("main:experience")
