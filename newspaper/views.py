from django.contrib.auth import get_user_model
from django.shortcuts import render

from newspaper.models import Newspaper, Topic, Redactor


def index(request):
    """Home page view for the Newspaper Agency."""

    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()
    num_redactors = get_user_model().objects.count()

    context = {
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        "num_redactors": num_redactors,
    }

    return render(request, "newspaper/index.html", context=context)
