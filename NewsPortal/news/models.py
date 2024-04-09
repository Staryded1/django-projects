from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Расчет рейтинга автора
        articles_rate = self.post_set.aggregate(Sum('news_rating'))['news_rating__sum'] or 0
        comments_rate = self.comment_set.aggregate(Sum('comment_rating'))['comment_rating__sum'] or 0
        self.rating = articles_rate * 3 + comments_rate
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    ARTICLES = 'AR'
    NEWS = 'NE'
    TYPES = [
        (NEWS, 'Новости'),
        (ARTICLES, 'Статьи')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice_types = models.CharField(max_length=2, choices=TYPES, default=NEWS)
    time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    news_title = models.CharField(max_length=255)
    news_text = models.TextField()
    news_rating = models.IntegerField(default=0)
    subscribers = models.ManyToManyField(User, related_name='subscribed_to', blank=True)

    def like(self):
        self.news_rating += 1
        self.save()

    def dislike(self):
        self.news_rating -= 1
        self.save()

    def preview(self):
        return self.news_text[:124] + '...' if len(self.news_text) > 124 else self.news_text

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_in_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

def send_email_notification(post):
    # Получаем список подписчиков этой категории
    subscribers = post.subscribers.all()

    # Формируем текст и заголовок письма
    subject = f"Новая статья в категории"
    message = f"Здравствуйте!\n\nНовая статья была опубликована в категории:\n\n{post.news_title}\n\n{post.news_text[:50]}..."
    
    # Создаем HTML-версию письма из шаблона
    html_message = render_to_string('email_notification.html', {'post': post})

    for subscriber in subscribers:
        # Отправляем письмо каждому подписчику
        send_mail(subject, strip_tags(message), None, [subscriber.email], html_message=html_message)

# Отправка приветственного письма при регистрации
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать!'
        message = render_to_string('registration/welcome_email.html', {
            'user': instance,
            'activate_url': reverse('activate', args=[instance.pk]),
        })
        send_mail(subject, strip_tags(message), None, [instance.email], html_message=message)
