import uuid
from django.db import models

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(
            upload_to="projects",
            blank=True, null=True, 
            help_text="16:9 pls"
        )
    description = models.TextField(blank=True, help_text="Write in Markdown!")
    skills = models.ManyToManyField("Skill", related_name="projects", blank=True)

    def __str__(self):
        return self.title
    
class Skill(models.Model):
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('experienced', 'Experienced'),
        ('advanced', 'Advanced'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, help_text="Write in Markdown!")
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, default='experienced')

    def __str__(self):
        return self.title
