from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class BaseViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Adm12345"
        )
        self.client.force_login(self.user)


class IndexViewTest(BaseViewTest):
    def test_index_view(self):
        response = self.client.get(reverse("newspaper:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper/index.html")
        self.assertIn("num_newspapers", response.context)
        self.assertIn("num_topics", response.context)
        self.assertIn("num_redactors", response.context)
