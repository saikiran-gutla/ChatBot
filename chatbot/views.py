from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json


# Create your views here.
def index(request):
    return render(request, 'chatbot/index.html')

@login_required
def room(request, room_name):
    return render(request, 'chatbot/room.html', {
        'room_name': room_name,
        "username": request.user.username
    })
# mark_safe(json.dumps(request.user.username)