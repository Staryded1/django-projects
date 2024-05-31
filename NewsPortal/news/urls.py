from django.urls import path
from .views import PostsList, PostDetail, SearchView, PostCreateView, PostUpdateView, PostDeleteView
from .views import SubscribeCategoryView
from .views import test_logging_view

urlpatterns = [
    # Пути к представлениям для новостей
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('subscribe/', SubscribeCategoryView.as_view(), name='subscribe_category'),
    path('test-logging/', test_logging_view, name='test_logging'),
]