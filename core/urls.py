from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.landing_page, name="landing_page"),

    path("create", views.create, name="create-user"),

    path("lobby", views.lobby, name="lobby"),

    path("lobby/handshake/<str:pk>", views.handshake, name="handshake"),

    path("room/<str:pk>", views.room, name="room"),

    path("decline", views.decline_notification, name="decline-note"),
]
