from django.forms import ModelForm, TextInput, Textarea, URLInput, SelectMultiple, DateInput,\
        ModelMultipleChoiceField
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError

from main.models import Project, Experience, Skill

class ProjectForm(ModelForm):
    skill_slugs = ModelMultipleChoiceField(
            queryset=Skill.objects.all(),
            to_field_name="title_slug",
            widget=SelectMultiple(),
            required=False,
            )
    class Meta:
        model = Project
        fields = [
            "title",
            "url",
            "thumbnail",
            "description",
            "skill_slugs",
        ]

        labels = {
            "title": "Project Name",
            "url": "URL to Project",
            "description": "Project Description",
            "thumbnail": "Thumbnail URL",
            "skill_slugs": "Related skills",
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
            # "skills": SelectMultiple(
            #     attrs={
            #         "placeholder": "Django",
            #     }
            # ),
        }
    
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("You think I don't know what you're doin??")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        return description

    def clean(self):
        cleaned_data = super().clean()

        # Older form submissions use the model field name and primary keys,
        # while the AJAX form submits slugs.  Supporting both keeps the form
        # endpoint backwards compatible.
        skill_ids = self.data.getlist("skills")
        if skill_ids:
            cleaned_data["skill_slugs"] = Skill.objects.filter(pk__in=skill_ids)

        return cleaned_data

    def save(self, commit=True):
        project = super().save(commit=commit)
        selected_skills = self.cleaned_data["skill_slugs"]

        if commit:
            project.skills.set(selected_skills)
        else:
            original_save_m2m = self.save_m2m

            def save_m2m():
                original_save_m2m()
                project.skills.set(selected_skills)

            self.save_m2m = save_m2m

        return project

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
    
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("You think I don't know what you're doin??")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        return description

class SkillForm(ModelForm):
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("You think I don't know what you're doin??")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        return description
