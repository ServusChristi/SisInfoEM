from django.urls import path
from . import views
from .views import PostUpdateView, blog_detail

urlpatterns = [
    path('', views.blog_index, name="blog_index"),
    path('post/<int:pk>/', views.blog_detail, name="blog_detail"),
    path('category/<category>/', views.blog_category, name="blog_category"),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/', blog_detail, name='blog_detail'),
    path('post/edit/<int:pk>/', PostUpdateView.as_view(), name='update_post'),
]