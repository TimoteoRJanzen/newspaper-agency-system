from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from newspaper.forms import RedactorCreationForm
from newspaper.models import Newspaper, Topic


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


class TopicListView(generic.ListView):
    model = Topic


class TopicDetailView(generic.DetailView):
    model = Topic
    queryset = Topic.objects.prefetch_related("newspapers")


class TopicCreateView(generic.CreateView):
    model = Topic
    fields = ["name"]
    success_url = reverse_lazy("newspaper:topic-list")


class TopicUpdateView(generic.UpdateView):
    model = Topic
    fields = ["name"]
    success_url = reverse_lazy("newspaper:topic-list")


class TopicDeleteView(generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("newspaper:topic-list")


class NewspaperListView(generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.select_related("topic").prefetch_related("publishers")


class NewspaperDetailView(generic.DetailView):
    model = Newspaper
    queryset = Newspaper.objects.select_related("topic").prefetch_related("publishers")


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    fields = ["title", "content", "topic", "publishers"]
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    fields = ["title", "content", "topic", "publishers"]


class NewspaperDeleteView(generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("newspaper:newspaper-list")


class RedactorListView(generic.ListView):
    model = get_user_model()


class RedactorDetailView(generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.prefetch_related("newspapers")


class RedactorCreateView(generic.CreateView):
    model = get_user_model()
    form_class = RedactorCreationForm
    success_url = reverse_lazy("newspaper:redactor-list")
