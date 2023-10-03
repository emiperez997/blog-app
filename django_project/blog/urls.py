from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('posts/', views.posts, name='posts'),
    path('post/create', views.create_post, name='post-create'),
    path('post/<int:id>/', views.post_detail, name='post-detail'),
    path('post/<int:id>/update', views.update_post, name='post-update'),
    path('post/<int:id>/delete', views.delete_post, name='post-delete'),
    path('about/', views.about, name='about'),
]
