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
        self.assertContains(
            response,
            f'href="{reverse("main:update_experience", args=[self.experience.pk])}"',
        )

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

    def test_update_experience_form_is_prefilled(self):
        response = self.client.get(
            reverse("main:update_experience", args=[self.experience.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/experience_edit_form.html")
        self.assertEqual(response.context["form"].instance, self.experience)
        self.assertContains(response, self.experience.title)

    def test_update_experience(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.pk]),
            {
                "title": "Senior Unit Tester",
                "description": "I now enjoy my job.", # yes i do after giving it all to codex lmao
                "category": "freelance",
                "thumbnail": "https://example.com/tester.png",
                "started_at": "2025-01-01",
                "ended_at": "2026-01-01",
            },
        )

        self.assertRedirects(response, reverse("main:experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Senior Unit Tester")
        self.assertEqual(self.experience.description, "I now enjoy my job.")
        self.assertEqual(self.experience.category, "freelance")
        self.assertEqual(self.experience.thumbnail, "https://example.com/tester.png")
        self.assertEqual(str(self.experience.started_at), "2025-01-01")
        self.assertEqual(str(self.experience.ended_at), "2026-01-01")

    def test_update_experience_rejects_invalid_data_without_changing_record(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.pk]),
            {"title": "", "description": "Updated description"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "title", "This field is required.")
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Unit Tester")

    def test_update_experience_returns_404_for_unknown_record(self):
        response = self.client.get(
            reverse("main:update_experience", args=[self.project.pk])
        )

        self.assertEqual(response.status_code, 404)

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
        self.assertContains(
            response,
            f'href="{reverse("main:update_project", args=[self.project.pk])}"',
        )

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:projects"))

        self.assertContains(response, "Nothing")

    def test_empty_description_project_page(self):
        self.project.description = ""
        self.project.save()
        response = self.client.get(reverse("main:projects"))

        self.assertContains(response, "No description was provided for this project.")
        
    # === Project (APIs) ===
    def test_get_projects_json(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["fields"]["title"], self.project.title)

    # === Project search ===
    def test_search_projects_by_title(self):
        other_project = Project.objects.create(
            title="Unrelated Project",
            description="This should not be returned by the search.",
        )

        response = self.client.get(reverse("main:projects"), {"title": "unit"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)
        self.assertNotContains(response, other_project.title)

    def test_search_projects_with_no_matches(self):
        response = self.client.get(reverse("main:projects"), {"title": "does not exist"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nothing's found...")
        self.assertNotContains(response, self.project.title)

    def test_clearing_project_search_returns_all_projects(self):
        other_project = Project.objects.create(title="Another Project")

        response = self.client.get(reverse("main:projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)
        self.assertContains(response, other_project.title)

    def test_create_project(self):
        response = self.client.post(reverse("main:create_project"), {
            "title": "Created Project",
            "description": "Created through the form.",
            "skills": [self.skill.pk],
        })

        self.assertRedirects(response, reverse("main:projects"))
        self.assertTrue(Project.objects.filter(title="Created Project").exists())

    def test_create_project_requires_a_title(self):
        project_count = Project.objects.count()

        response = self.client.post(reverse("main:create_project"), {
            "description": "A project without a title.",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "title", "This field is required.")
        self.assertEqual(Project.objects.count(), project_count)

    def test_update_project_form_is_prefilled(self):
        response = self.client.get(reverse("main:update_project", args=[self.project.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/projects_edit_form.html")
        self.assertEqual(response.context["form"].instance, self.project)
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.skill.title)

    def test_update_project(self):
        new_skill = Skill.objects.create(
            title="Regression Testing",
            description="Tests after edits.",
            proficiency="experienced",
        )

        response = self.client.post(
            reverse("main:update_project", args=[self.project.pk]),
            {
                "title": "An Updated Unit Test",
                "url": "https://example.com/project",
                "thumbnail": "https://example.com/project.png",
                "description": "Updated through the edit form.",
                "skills": [new_skill.pk],
            },
        )

        self.assertRedirects(response, reverse("main:projects"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "An Updated Unit Test")
        self.assertEqual(self.project.url, "https://example.com/project")
        self.assertEqual(self.project.thumbnail, "https://example.com/project.png")
        self.assertEqual(self.project.description, "Updated through the edit form.")
        self.assertQuerySetEqual(self.project.skills.all(), [new_skill])

    def test_update_project_rejects_invalid_data_without_changing_record(self):
        response = self.client.post(
            reverse("main:update_project", args=[self.project.pk]),
            {"title": "", "description": "Updated description"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "title", "This field is required.")
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "A Unit Test")

    def test_update_project_returns_404_for_unknown_record(self):
        response = self.client.get(
            reverse("main:update_project", args=[self.experience.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_project(self):
        response = self.client.post(
            reverse("main:delete_project", args=[self.project.pk])
        )

        self.assertRedirects(response, reverse("main:projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_get_delete_project_does_not_delete(self):
        response = self.client.get(
            reverse("main:delete_project", args=[self.project.pk])
        )

        self.assertRedirects(response, reverse("main:projects"))
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())
                    
    # === Skill ===
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
