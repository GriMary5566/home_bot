from django.contrib import admin

from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat_name', 'role')
    list_filter = ('chat_name', 'role', 'created_date')
    search_fields = ('chat_name',)
    empty_value_display = '-пусто-'


admin.site.register(Message, MessageAdmin)
