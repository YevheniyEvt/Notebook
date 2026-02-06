from django.urls import path

from notes import views

app_name = "notes"

urlpatterns = [
    path("topics/", views.TopicListView.as_view(), name="topic_list"),
    path("topic/create/", views.TopicCreateView.as_view(), name="topic_create"),
    path("topic/<int:pk>/update/", views.TopicUpdateView.as_view(), name="topic_update"),
    path("topic/<int:pk>/delete/", views.TopicDeleteView.as_view(), name="topic_delete"),


    path("topic/<int:pk>/section/create/", views.SectionCreateView.as_view(), name="section_create"),
    path("topic/<int:pk>/sections/", views.SectionListView.as_view(), name="sections_list"),
    path("section/<int:pk>/", views.SectionDetail.as_view(), name="section_detail"),
    path("section/<int:pk>/update/", views.SectionUpdateView.as_view(), name="section_update"),
    path("section/<int:pk>/delete/", views.SectionDeleteView.as_view(), name="section_delete"),


    path("section/<int:pk>/codes/", views.SectionCodeListView.as_view(), name="code_list"),
    path("section/<int:pk>/code/create/", views.SectionCodeCreateView.as_view(), name="code_create"),
    path("code/<int:pk>/update/", views.SectionCodeUpdateView.as_view(), name="code_update"),
    path("code/<int:pk>/delete/", views.SectionCodeDeleteView.as_view(), name="code_delete"),


    path("section/<int:pk>/articles/", views.SectionArticleListView.as_view(), name="article_list"),
    path("section/<int:pk>/article/create/", views.SectionArticleCreateView.as_view(), name="article_create"),
    path("article/<int:pk>/update/", views.SectionArticleUpdateView.as_view(), name="article_update"),
    path("article/<int:pk>/delete/", views.SectionArticleDeleteView.as_view(), name="article_delete"),


    path("section/<int:pk>/links/", views.SectionLinksListView.as_view(), name="link_list"),
    path("section/<int:pk>/link/create/", views.SectionLinksCreateView.as_view(), name="link_create"),
    path("link/<int:pk>/update/", views.SectionLinksUpdateView.as_view(), name="link_update"),
    path("link/<int:pk>/delete/", views.SectionLinksDeleteView.as_view(), name="link_delete"),


    path("section/<int:pk>/images/", views.SectionImageListView.as_view(), name="image_list"),
    path("section/<int:pk>/image/create/", views.SectionImageCreateView.as_view(), name="image_create"),
    path("image/<int:pk>/update/", views.SectionImageUpdateView.as_view(), name="image_update"),
    path("image/<int:pk>/delete/", views.SectionImageDeleteView.as_view(), name="image_delete"),

]