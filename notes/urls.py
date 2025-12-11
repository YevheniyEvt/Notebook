from django.urls import path

from notes.views import TopicListView, TopicDetail, SectionDetail, SectionCodeListView, SectionArticleListView, \
    SectionLinksListView, SectionImageListView

app_name = "notes"

urlpatterns = [
    path("topics/", TopicListView.as_view(), name="topic_list"),
    path("topic/<int:pk>/sections/", TopicDetail.as_view(), name="topic_detail"),
    path("section/<int:pk>/", SectionDetail.as_view(), name="section_detail"),

    path("section/<int:pk>/codes/", SectionCodeListView.as_view(), name="code_list"),
    path("section/<int:pk>/articles/", SectionArticleListView.as_view(), name="article_list"),
    path("section/<int:pk>/links/", SectionLinksListView.as_view(), name="link_list"),
    path("section/<int:pk>/images/", SectionImageListView.as_view(), name="image_list"),

]