from django.contrib import admin

from .models import BotMessage


class BotMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat_name', 'role', 'content_tokens')
    list_filter = ('user', 'chat_name', 'role', 'created_date')
    search_fields = ('user', 'chat_name',)
    empty_value_display = '-пусто-'


admin.site.register(BotMessage, BotMessageAdmin)
