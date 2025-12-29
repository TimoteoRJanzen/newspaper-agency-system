from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminBaseTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="Admin12345"
        )
        self.client.force_login(self.admin_user)


class RedactorAdminTest(AdminBaseTest):
    def setUp(self):
        super().setUp()
        self.redactor = get_user_model().objects.create_user(
            username="john",
            password="Test12345",
            first_name="John",
            last_name="Doe",
            years_of_experience=5
        )

    def test_redactor_listed(self):
        url = reverse("admin:newspaper_redactor_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_years_of_experience_listed_in_admin_detail(self):
        url = reverse(
            "admin:newspaper_redactor_change",
            args=[self.redactor.id]
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Years of experience")
        self.assertContains(response, self.redactor.years_of_experience)
