from django.contrib.auth.models import AbstractUser
from django.db import models

class ChatUser(AbstractUser):
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']
    def __str__(self):
        return f'Пользователь {self.username}'
