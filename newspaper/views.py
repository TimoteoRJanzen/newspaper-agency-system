from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from newspaper.forms import (
    RedactorCreationForm,
    RedactorUpdateForm,
    RedactorSearchForm, NewspaperSearchForm, TopicSearchForm
)
from newspaper.models import Newspaper, Topic

Redactor = get_user_model()

def index(request):
    """Home page view for the Newspaper Agency."""

    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()
    num_redactors = Redactor.objects.count()

    context = {
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        "num_redactors": num_redactors,
    }

    return render(request, "newspaper/index.html", context=context)


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 5

    def get_queryset(self):
        queryset = Topic.objects.all()
        form = TopicSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TopicSearchForm(
            initial={"name": self.request.GET.get("name", "")}
        )
        return context



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
    paginate_by = 5

    def get_queryset(self):
        queryset = (
            Newspaper.objects
            .select_related("topic")
            .prefetch_related("publishers")
        )

        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = NewspaperSearchForm(
            initial={"title": self.request.GET.get("title", "")}
        )
        return context


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
    model = Redactor
    paginate_by = 5

    def get_queryset(self):
        queryset = Redactor.objects.all()
        form = RedactorSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = RedactorSearchForm(
            initial={
                "username": self.request.GET.get("username", "")
            }
        )
        return context


class RedactorDetailView(generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspapers")


class RedactorCreateView(generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("newspaper:redactor-list")


class RedactorUpdateView(generic.UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm
    success_url = reverse_lazy("newspaper:redactor-list")


class RedactorDeleteView(generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("newspaper:redactor-list")
