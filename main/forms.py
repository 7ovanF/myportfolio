from django.forms import ModelForm, TextInput, Textarea, URLInput, SelectMultiple, DateInput

from main.models import Project, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "url",
            "thumbnail",
            "description",
            "skills",
        ]

        labels = {
            "title": "Project Name",
            "url": "URL to Project",
            "description": "Project Description",
            "thumbnail": "Thumbnail URL",
            "skills": "Related skills",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "url": URLInput(
                attrs={
                    "placeholder": "https://github.com/torvalds/linux",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000 (16:9 pls)",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Format in markdown!",
                    "rows": 5,
                }
            ),
            "skills": SelectMultiple(
                attrs={
                    "placeholder": "Django",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Experience Name",
            "description": "Experience Description",
            "category": "Type of experience",
            "thumbnail": "Thumbnail URL",
            "started_at": "Start date",
            "ended_at": "End date",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Sysadmin",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Format in markdown!",
                    "rows": 5,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000 (16:9 pls)",
                }
            ),
            "started_at": DateInput(
                attrs={
                    "placeholder": "2026-06-14"
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "placeholder": "2028-06-14 (blank for unfinished)"
                }
            )
        }