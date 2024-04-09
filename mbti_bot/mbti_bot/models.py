from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

class MBTI_type(models.Model):
    text = models.TextField()
    description = models.TextField()



# class Group(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(
#         max_length=150,
#         unique=True
#     )
#     description = models.TextField()

#     def __str__(self):
#         return self.title


# class Post(models.Model):
#     text = models.TextField(
#         verbose_name='Текст поста',
#         help_text='Введите текст поста'
#     )
#     pub_date = models.DateTimeField(
#         verbose_name='Дата публикации',
#         auto_now_add=True
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name='Автор'
#     )

#     group = models.ForeignKey(
#         Group,
#         blank=True,
#         null=True,
#         on_delete=models.SET_NULL,
#         related_name='posts',
#         verbose_name='Группа',
#         help_text='Группа, к которой будет относиться пост'
#     )

#     def __str__(self):
#         return self.text[:15]

#     class Meta:
#         ordering = ['-pub_date']
#         default_related_name = 'posts'
