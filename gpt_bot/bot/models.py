from django.db import models

class Message(models.Model):
    chat_id = models.CharField(
        max_length=10,
        verbose_name='id чата'
    )
    chat_name = models.CharField(
        max_length=200,
        verbose_name='Имя чата'
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

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_date', '-id']
    
    def __str__(self):
        return f'Сообщение {self.chat_name}.'
