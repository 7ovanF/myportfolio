from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Project, Skill, Experience


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
                title="Unit Tester",
                description="i hate my job",
                category="full-time",
                started_at="2026-09-11",
            )

        self.project = Project.objects.create(
                title="A Unit Test",
                description="i still hate it",
            )

        self.skill = Skill.objects.create(
                title="Unit Testing",
                description="damn",
                proficiency="advanced",
            )

        self.project.skills.add(self.skill)

    # === General ===
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:landing_page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/profile.html")
        self.assertContains(response, f'href="{reverse("main:experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    # === Experience ===
    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Unit Tester")
        self.assertEqual(self.experience.category, "full-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.category)
        self.assertContains(response, "active (running)")
        self.assertContains(response, f'href="{reverse("main:landing_page")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:experience"))

        self.assertContains(response, "You could say this guy is... inexperienced")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "inactive (dead)")

    # === Project ===
    def test_project_model(self):
        self.assertEqual(str(self.project), "A Unit Test")
        self.assertEqual(self.project.skills.first(), self.skill)

    def test_project_page(self):
        response = self.client.get(reverse("main:projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/projects.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, "unit-testing")
        self.assertContains(response, f'href="{reverse("main:landing_page")}"')

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:projects"))

        self.assertContains(response, "Oopsies, nothing interesting has happened in this guy's life...")

    def test_empty_description_project_page(self):
        self.project.description = ""
        self.project.save()
        response = self.client.get(reverse("main:projects"))

        self.assertContains(response, "No description was provided for this project.")
                    
    # === Project ===
    def test_skill_model(self):
        self.assertEqual(str(self.skill), "Unit Testing")
        self.assertEqual(self.skill.proficiency, "advanced")

    def test_skills_on_project_page(self):
        response = self.client.get(reverse("main:projects"))

        self.assertContains(response, "unit-testing")
        
    def test_empty_skills_on_project_page(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:projects"))

        self.assertNotContains(response, "unit-testing")