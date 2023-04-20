from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BotMessage(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    chat_id = models.CharField(
        max_length=10,
        verbose_name='id чата',
        blank=True
    )
    chat_name = models.CharField(
        max_length=200,
        verbose_name='Имя чата',
        blank=True
    )
    created_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    role = models.CharField(
        max_length=20,
        verbose_name='Роль в модели ChatGpt'
    )
    content = models.TextField(
        verbose_name='Текст сообщения'
    )
    content_tokens = models.PositiveIntegerField(
        verbose_name='Количество токенов в сообщении',
        default=1
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_date', '-id']

    def __str__(self):
        if self.user.username == 'Bot':
            return f'Сообщение от {self.chat_name}.'
        return f'Сообщение от {self.user.username}.'
