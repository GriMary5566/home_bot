# Generated by Django 3.2.18 on 2023-05-09 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(blank=True, max_length=10, verbose_name='id чата')),
                ('chat_name', models.CharField(blank=True, max_length=200, verbose_name='Имя чата')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('role', models.CharField(max_length=20, verbose_name='Роль в модели ChatGpt')),
                ('content', models.TextField(verbose_name='Текст сообщения')),
                ('content_tokens', models.PositiveIntegerField(default=1, verbose_name='Количество токенов в сообщении')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['-created_date', '-id'],
            },
        ),
    ]
