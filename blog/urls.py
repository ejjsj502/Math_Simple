from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    path('post/<int:post_pk>/comment/add/', views.add_comment, name='comment-add'),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', views.category_detail, name='category-detail'),
]