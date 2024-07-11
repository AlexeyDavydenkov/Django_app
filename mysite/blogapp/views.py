from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .models import Article
from .forms import ArticleForm


class BasedView(ListView):
    template_name = 'blogapp/article_list.html'
    context_object_name = 'article'
    queryset = Article.objects.select_related('author', 'category').prefetch_related('tags').defer('content')


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("blogapp:blogs")