from django.shortcuts import render

# импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView

# импортируем модель Product из models.py
from .models import Post
from .forms import SearchForm
from django.views.generic import FormView
from .forms import PostForm
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


# создадим модель объектов, которые будем выводить
class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10  # Устанавливаем количество новостей на странице'

    #
    context_object_name = 'news'


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10  # Определяем количество новостей на странице

class SearchView(ListView):
    model = Post
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(title__icontains=query)
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context

class SearchView(FormView):
    template_name = 'search.html'
    form_class = SearchForm

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        author = form.cleaned_data.get('author')
        date = form.cleaned_data.get('date')

        # Фильтрация объектов модели Post по введенным критериям
        posts = Post.objects.all()
        if title:
            posts = posts.filter(news_title__icontains=title)
        if author:
            posts = posts.filter(author__icontains=author)
        if date:
            posts = posts.filter(time_in__date=date)

        # Передача отфильтрованных объектов в контекст шаблона
        return render(self.request, self.template_name, {'form': form, 'posts': posts})
    
class PostCreateView(CreateView):
    model = Post
    fields = ['author', 'choice_types', 'news_title', 'news_text', 'categories']
    template_name = 'post_create.html'
    success_url = reverse_lazy('posts_list')  # Перенаправляем на страницу списка после успешного создания

class PostUpdateView(UpdateView):
    model = Post
    fields = ['author', 'choice_types', 'news_title', 'news_text', 'categories']
    template_name = 'post_update.html'
    success_url = reverse_lazy('posts_list')  # Перенаправляем на страницу списка после успешного редактирования

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('posts_list')  # Перенаправляем на страницу списка после успешного удаления