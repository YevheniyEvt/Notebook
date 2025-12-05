from django.urls import path

from daybook.views import EntriesList, EntriesUpdateView, EntriesCreateView

app_name = "daybook"

urlpatterns = [
    path("entries/", EntriesList.as_view(), name="entries_list"),
    path("entry/create/", EntriesCreateView.as_view(), name="entries_create"),
    path("entry/update/<int:pk>", EntriesUpdateView.as_view(), name="entries_update"),
]