# Generated by Django 3.2.18 on 2023-04-20 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_botmessage_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botmessage',
            name='chat_id',
            field=models.CharField(blank=True, max_length=10, verbose_name='id чата'),
        ),
        migrations.AlterField(
            model_name='botmessage',
            name='chat_name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Имя чата'),
        ),
    ]
