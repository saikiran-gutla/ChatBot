import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, ConnectionHistory
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        print('THIS IS FETCH MESSAGES', data)
        messages = Message.last_10_mesages(self)
        content = {
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_messages(self, data):
        author = data['from']
        print('THIS IS NEW MESSAGES', author)
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(author=author_user, content=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def set_status(self, data):
        print('THIS IS SET STATUS', data)
        status = data['status']
        author = data['username']
        author_user = User.objects.filter(username=author)[0]
        connection_stauts = ConnectionHistory.objects.filter(user=author_user).values('user', 'status', 'last_echo')
        print(f"T- DATA : {connection_stauts}")
        print('THIS IS AUTHOR USER', author_user)
        for q in connection_stauts:
            print(f"ASDF: {q}")
            content = {
                'messages': self.status_to_json(q)
            }
            self.send_message(content)
        status_update = ConnectionHistory.objects.get(user=author_user)
        status_update.status = status
        status_update.save()

    def typing(self, data):
        status = data['type_status']
        author = self.scope['user']
        print('THIS IS SET STATUS', data, "USER ", author)
        author_user = User.objects.filter(username=author)[0]
        connection_status = ConnectionHistory.objects.filter(user=author_user).values('user', 'typing_status', 'status',
                                                                         'last_echo')
        print(f"T- DATA : {connection_status}")
        print('THIS IS AUTHOR USER', author_user)
        for q in connection_status:
            print(f"ASDF: {q}")
            content = {
                'messages': self.status_to_json(q)
            }
            self.send_message(content)
        status_update = ConnectionHistory.objects.get(user=author_user)
        status_update.typing_status = status
        status_update.save()

    commands = {
        'fetch_messages': fetch_messages,
        'new_messages': new_messages,
        'set_status': set_status,
        'typing': typing,
    }

    def status_to_json(self, connectionstatus):
        print(f"STATUS TO JSON : {connectionstatus}")
        return {
            'author': connectionstatus['user'],
            'status': connectionstatus['status'],
            'last_login': str(connectionstatus['last_echo'])
        }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        print(f"MESSAGES TO JSON  : {result}")
        return result

    def message_to_json(self, message):
        # message here is an object , we need to deserialize it
        print(f"MESSAGE TO JSON  : {message.author.username}"
              f"\t {message.content} \t {str(message.time_stamp)}")
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.time_stamp)
        }

    def connect(self):
        print("CONNECTION IS MADE FOR ", self.scope['user'])
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.set_status(data={'status': 'online', 'username': self.scope['user']})

    def disconnect(self, close_code):
        # Leave room group
        print("DISCONNECTED ")
        self.set_status(data={'status': 'offline', 'username': self.scope['user']})
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        print(f"RECEIVE DATA  : {data}")
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        print("SENDING CHAT MESSAGES")
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        print("SEND MESSAGE")
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        print("CHAT MESSAGE")
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
