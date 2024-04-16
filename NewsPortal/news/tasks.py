from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Post
from django.contrib.auth.models import User  # Импортируем модель User, если она еще не импортирована
from datetime import datetime, timedelta
from django.utils import timezone


@shared_task
def send_notification_email(post_id):
    post = Post.objects.get(pk=post_id)
    # Получаем список подписчиков этой категории
    subscribers = post.subscribers.all()

    # Формируем текст и заголовок письма
    subject = f"Новая статья в категории '{post.categories.first().name}'"
    message = f"Здравствуйте!\n\nНовая статья была опубликована в категории '{post.categories.first().name}':\n\n{post.news_title}\n\n{post.news_text[:50]}..."
    
    # Создаем HTML-версию письма из шаблона
    html_message = render_to_string('email_notification.html', {'post': post})

    for subscriber in subscribers:
        # Отправляем письмо каждому подписчику
        send_mail(subject, strip_tags(message), None, [subscriber.email], html_message=html_message)

@shared_task
def send_weekly_newsletter():
    # Определяем временной интервал для выборки последних новостей (например, за последнюю неделю)
    start_date = timezone.now() - timedelta(days=7)
    end_date = timezone.now()

    # Получаем все новости за последнюю неделю
    latest_posts = Post.objects.filter(time_in__range=(start_date, end_date))

    # Формируем текст и заголовок письма
    subject = "Еженедельная рассылка новостей"
    context = {'latest_posts': latest_posts}
    html_message = render_to_string('welcome_email.html', context)

    # Отправляем письмо подписчикам
    subscribers = User.objects.all()  
    for subscriber in subscribers:
        send_mail(subject, strip_tags(html_message), None, [subscriber.email], html_message=html_message)