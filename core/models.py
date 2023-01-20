from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser, models.Model):
    date_created = models.DateTimeField(auto_now=True)


class Room(models.Model):
    room_id = models.CharField(max_length=5)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player1")
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player2")


class Notification(models.Model):
    sending_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiving_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    message = models.CharField(max_length=50)