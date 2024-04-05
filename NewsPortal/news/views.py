from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from .forms import SearchForm, PostForm
from django.views.generic import FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10


class SearchView(ListView):
    model = Post
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(news_title__icontains=query)
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('posts_list')
    permission_required = 'news.add_post'


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_update.html'
    success_url = reverse_lazy('posts_list')
    permission_required = 'news.change_post'


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('posts_list')
    permission_required = 'news.delete_post'
