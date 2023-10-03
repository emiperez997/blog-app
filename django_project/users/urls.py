from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_blog, name='login'),
    path('logout/', views.logout_blog, name='logout'),
    path('register/', views.register_blog, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('<str:username>/posts', views.user_posts, name='user-posts')
]
