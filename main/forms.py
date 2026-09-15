from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Project

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
                    "rows": 5, # todo
                }
            ),
            # "tech_stack": TextInput(
            #     attrs={
            #         "placeholder": "Django, Python, HTML, CSS",
            #     }
            # ),
        }