from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from notes.models import Section, Topic, Code, Article, Links, Image


# Create your views here.

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TopicDetail(DetailView):
    model = Topic
    context_object_name = 'topic'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class SectionDetail(DetailView):
    model = Section
    context_object_name = 'section'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class SectionCodeListView(ListView):
    model = Code
    context_object_name = 'codes'
    template_name = 'notes/partials/code_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)


class SectionArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'notes/partials/article_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)


class SectionLinksListView(ListView):
    model = Links
    context_object_name = 'links'
    template_name = 'notes/partials/links_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)


class SectionImageListView(ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'notes/partials/images_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)