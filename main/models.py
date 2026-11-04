import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, unique=True)
    url = models.URLField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True, help_text="16:9 pls")
    description = models.TextField(blank=True, help_text="Write in Markdown!")
    skills = models.ManyToManyField("Skill", related_name="projects", blank=True)
    starred_by = models.ManyToManyField(
        User, related_name="starred_projects", blank=True
    )

    def __str__(self):
        return self.title
    
class Skill(models.Model):
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('experienced', 'Experienced'),
        ('advanced', 'Advanced'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, unique=True)
    title_slug = models.CharField(max_length=255, unique=True) # auto-determined, not available in forms`
    description = models.TextField(blank=True, help_text="Write in Markdown!")
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, default='experienced')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        self.validate_unique()
        super().save(*args, **kwargs)

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Write in Markdown!")
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True, help_text="16:9 pls")
    started_at = models.DateField()
    ended_at = models.DateField(blank=True, null=True)
    starred_by = models.ManyToManyField(
        User, related_name="starred_experiences", blank=True
    )

    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None
