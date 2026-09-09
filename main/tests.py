from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Project


# Jujur belum disentuh, sibuk mmf
class MainTest(TestCase):
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:landing_page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, f'href="{reverse("main:projects")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)