from django.contrib.auth import get_user_model
from django.test import TestCase

from newspaper.models import Topic, Newspaper


class ModelsTest(TestCase):
    def test_redactor_str(self):
        redactor = get_user_model().objects.create_user(
            username="redactor_test",
            password="Test12345",
        )
        self.assertEqual(str(redactor), redactor.username)

    def test_create_redactor_with_years_of_experience(self):
        username = "redactor_exp"
        password = "Test12345"
        years_of_experience = 5

        redactor = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience,
        )

        self.assertEqual(redactor.years_of_experience, years_of_experience)

    def test_topic_str(self):
        topic = Topic.objects.create(name="Technology")
        self.assertEqual(str(topic), topic.name)

    def test_newspaper_str(self):
        newspaper = Newspaper.objects.create(
            title="Daily Tech",
            content="Tech content",
        )
        self.assertEqual(str(newspaper), newspaper.title)
