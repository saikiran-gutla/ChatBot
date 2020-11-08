from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Chat, Contact


# Create your views here.
def index(request):
    return render(request, 'chatbot/index.html')


@login_required
def room(request, room_name):
    return render(request, 'chatbot/chat.html', {
        'room_name': room_name,
        "username": request.user.username
    })


# mark_safe(json.dumps(request.user.username)

User = get_user_model()


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
