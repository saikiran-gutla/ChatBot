from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models

User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(
        User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    contact = models.ForeignKey(
        Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username

    def last_10_mesages(self):
        return Message.objects.order_by('-time_stamp').all()[:10]


class ConnectionHistory(models.Model):
    ONLINE = 'online'
    OFFLINE = 'offline'
    STATUS = (
        (ONLINE, 'On-line'),
        (OFFLINE, 'Off-line'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    device_id = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10, choices=STATUS,
        default=ONLINE
    )
    first_login = models.DateTimeField(auto_now_add=True)
    last_echo = models.DateTimeField(auto_now=True)
    typing_status = models.BooleanField(default=False)

    class Meta:
        unique_together = (("user", "device_id"),)

    def __str__(self):
        return '%s %s %s' % (self.user, self.status, str(self.last_echo))

    def Userstatus(self):
        return ConnectionHistory.objects.all()


class Chat(models.Model):
    participants = models.ManyToManyField(
        Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)
