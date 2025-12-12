from django.urls import path

from notes import views

app_name = "notes"

urlpatterns = [
    path("topics/", views.TopicListView.as_view(), name="topic_list"),
    path("topic/<int:pk>/sections/", views.TopicDetail.as_view(), name="topic_detail"),
    path("topic/create/", views.TopicCreateView.as_view(), name="topic_create"),
    path("topic/<int:pk>/update/", views.TopicUpdateView.as_view(), name="topic_update"),
    path("topic/<int:pk>/delete/", views.TopicDeleteView.as_view(), name="topic_delete"),

    path("section/<int:pk>/", views.SectionDetail.as_view(), name="section_detail"),

    path("section/<int:pk>/codes/", views.SectionCodeListView.as_view(), name="code_list"),
    path("section/<int:pk>/articles/", views.SectionArticleListView.as_view(), name="article_list"),
    path("section/<int:pk>/links/", views.SectionLinksListView.as_view(), name="link_list"),
    path("section/<int:pk>/images/", views.SectionImageListView.as_view(), name="image_list"),

]