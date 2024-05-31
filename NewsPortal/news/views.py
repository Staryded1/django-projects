from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category
from .forms import SearchForm, PostForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic.base import View
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from .models import send_email_notification
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    # Применяем кэширование на 5 минут
    @cache_page(300)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    # Применяем кэширование на 5 минут или пока статья не изменится
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

    @method_decorator(cache_page(300))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    # Применяем кэширование на 5 минут
    @cache_page(300)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


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

    def form_valid(self, form):
        # Проверяем количество опубликованных новостей пользователя за последние 24 часа
        user = self.request.user
        posts_count = Post.objects.filter(author__user=user, time_in__gte=timezone.now() - timedelta(days=1)).count()
        if posts_count >= 3:
            return HttpResponseBadRequest("Вы не можете публиковать более трех новостей в сутки.")

        # Вызываем сохранение формы, чтобы получить объект Post
        self.object = form.save(commit=False)
        self.object.author = user.author  # Привязываем автора
        self.object.save()

        # Отправляем уведомление подписчикам
        send_email_notification(self.object)

        return HttpResponseRedirect(self.get_success_url())


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

class SubscribeCategoryView(View):
    def post(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        user = request.user
        if user.is_authenticated:
            if user in category.subscribers.all():
                category.subscribers.remove(user)
                subscribed = False
            else:
                category.subscribers.add(user)
                subscribed = True
            return JsonResponse({'subscribed': subscribed})
        else:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)

    # Применяем кэширование на 1 минуту
    @cache_page(60)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        
def subscribe_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        if request.user in category.subscribers.all():
            category.subscribers.remove(request.user)
            subscribed = False
        else:
            category.subscribers.add(request.user)
            subscribed = True
        return JsonResponse({'subscribed': subscribed})
    
import logging
from django.http import HttpResponse

# Получаем логгер с именем 'django'
logger = logging.getLogger('django')

def test_logging_view(request):
    # Логируем сообщения разных уровней
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    
    return HttpResponse("Logging test complete. Check your logs.")
