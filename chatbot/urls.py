from django.contrib import admin
from django.urls import path, include
from chatbot import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),

]
