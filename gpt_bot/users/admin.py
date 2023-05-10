from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import BotUser


class BotUserAdmin(UserAdmin):
    list_display = ('id', 'username',)
    list_filter = ('username',)
    search_fields = ('username',)


admin.site.register(BotUser, BotUserAdmin)
