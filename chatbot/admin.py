from django.contrib import admin
from .models import Message, ConnectionHistory


# Register your models here.
class ConnectionHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "device_id", "status", "typing_status", "first_login", "last_echo"]


admin.site.register(Message)
admin.site.register(ConnectionHistory, ConnectionHistoryAdmin)

from .models import Contact, Chat, Message

admin.site.register(Chat)
admin.site.register(Contact)
admin.site.register(Message)
