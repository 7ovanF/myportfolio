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
    thumbnail = models.ImageField(
            upload_to="experience",
            blank=True, null=True, 
            help_text="16:9 pls"
        )
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None