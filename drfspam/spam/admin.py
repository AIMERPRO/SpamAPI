from django.contrib import admin

from spam.models import Spam, Client, Message


@admin.register(Spam)
class SpamAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "filter")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "code", "tag", "UTC")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "spam_id", "client_id")