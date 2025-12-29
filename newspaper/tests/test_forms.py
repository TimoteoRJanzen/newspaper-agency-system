from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper.models import Topic, Newspaper


TOPIC_URL = reverse("newspaper:topic-list")
NEWSPAPER_URL = reverse("newspaper:newspaper-list")
REDACTOR_URL = reverse("newspaper:redactor-list")


class TopicSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Adm12345"
        )
        self.client.force_login(self.user)

        self.topic_match = Topic.objects.create(name="Technology")
        self.topic_no_match = Topic.objects.create(name="Sports")

    def test_search_topic_by_name(self):
        response = self.client.get(
            TOPIC_URL,
            {"name": "Tech"}
        )

        self.assertEqual(response.status_code, 200)

        topic_list = response.context["topic_list"]

        self.assertIn(self.topic_match, topic_list)
        self.assertNotIn(self.topic_no_match, topic_list)


class NewspaperSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Adm12345"
        )
        self.client.force_login(self.user)

        self.newspaper_match = Newspaper.objects.create(
            title="Tech Daily",
            content="Tech news"
        )

        self.newspaper_no_match = Newspaper.objects.create(
            title="Sports Weekly",
            content="Sports news"
        )

    def test_search_newspaper_by_title(self):
        response = self.client.get(
            NEWSPAPER_URL,
            {"title": "Tech"}
        )

        self.assertEqual(response.status_code, 200)

        newspaper_list = response.context["newspaper_list"]

        self.assertIn(self.newspaper_match, newspaper_list)
        self.assertNotIn(self.newspaper_no_match, newspaper_list)


class RedactorSearchTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user(
            username="admin",
            password="Adm12345"
        )
        self.client.force_login(self.admin)

        self.redactor_match = get_user_model().objects.create_user(
            username="john_doe",
            password="test12345"
        )

        self.redactor_no_match = get_user_model().objects.create_user(
            username="maria_silva",
            password="test12345"
        )

    def test_search_redactor_by_username(self):
        response = self.client.get(
            REDACTOR_URL,
            {"username": "john"}
        )

        self.assertEqual(response.status_code, 200)

        redactor_list = response.context["redactor_list"]

        self.assertIn(self.redactor_match, redactor_list)
        self.assertNotIn(self.redactor_no_match, redactor_list)
