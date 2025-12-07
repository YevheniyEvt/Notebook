from django.urls import path

from daybook.views import (
    EntriesListView,
    EntriesUpdateView,
    EntriesCreateView,
    EntriesDetailView,
    EntriesDeleteView
)

app_name = "daybook"

urlpatterns = [
    path("entries/", EntriesListView.as_view(), name="entries_list"),
    path("entry/<int:pk>", EntriesDetailView.as_view(), name="entries_detail"),
    path("entry/create/", EntriesCreateView.as_view(), name="entries_create"),
    path("entry/update/<int:pk>", EntriesUpdateView.as_view(), name="entries_update"),
    path("entry/delete/<int:pk>", EntriesDeleteView.as_view(), name="entries_delete"),
]