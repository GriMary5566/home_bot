from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ChatUser


class ChatUserAdmin(UserAdmin):
    list_display = ('id', 'username',)
    list_filter = ('username',)
    search_fields = ('username',)


admin.site.register(ChatUser, ChatUserAdmin)
