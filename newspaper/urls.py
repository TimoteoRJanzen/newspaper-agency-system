from django.urls import path
from newspaper.views import (
    index,
    TopicListView,
    NewspaperListView
)

app_name = "newspaper"

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
]
