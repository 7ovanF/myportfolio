from django.shortcuts import render

from .models import Project, Experience

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
    context = {
            "active_page": "landing_page",
            **base_context, **profile_context,
            "project_list": Project.objects.all(),
            "experience_list": Experience.objects.all(),
        }
    return render(request, "main/profile.html", context)

def projects(request):
    context = {
            "active_page": "projects",
            **base_context,
            "project_list": Project.objects.all(),
        }
    return render(request, "main/projects.html", context)

def experience(request):
    context = {
            "active_page": "experience",
            **base_context,
            "experience_list": Experience.objects.all(),
        }
    return render(request, "main/experience.html", context)