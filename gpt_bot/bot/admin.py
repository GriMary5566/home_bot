from django.contrib import admin

from .models import BotMessage

class BotMessageAdmin(admin.ModelAdmin):
    list_display = ('chat_name', 'role', 'content_tokens')
    list_filter = ('chat_name', 'role', 'created_date')
    search_fields = ('chat_name',)
    empty_value_display = '-пусто-'


admin.site.register(BotMessage, BotMessageAdmin)
