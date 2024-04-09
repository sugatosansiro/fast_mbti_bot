"""mbti_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# from django.contrib import admin
# from django.urls import include, path

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('posts.urls', namespace='posts')),
#     path('auth/', include('users.urls', namespace='users')),
#     path('auth/', include('django.contrib.auth.urls')),
#     path('about/', include('about.urls', namespace='about')),
# ]


# from django.urls import path
# from posts import views

# app_name = 'posts'

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('group/<slug:slug>/', views.group_posts, name='group_list'),
#     path('profile/<str:username>/', views.profile, name='profile'),
#     path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
#     path('create/', views.post_create, name='post_create'),
#     path('posts/<post_id>/edit/', views.post_edit, name='post_edit'),
# ]
