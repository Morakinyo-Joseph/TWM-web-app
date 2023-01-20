from django.shortcuts import render, redirect
from .models import User, Room, Notification
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import string
import random

# Create your views here.

def landing_page(request):
    return render(request, "core/landing_page.html")


def create(request):
    if request.method == "POST":
        username = request.POST["user"]
        password = "password"
        email = "email@email.com"

        User.objects.create_user(username=username, first_name="firstname", last_name="lastname", password=password, email=email)

        the_user = authenticate(username=username, password=password)
        login(request, the_user)

        return redirect("core:lobby")

    return render(request, "core/create-user.html")



def lobby(request):
    all_user = User.objects.all()

    notify = None

    flag = False # becomes false if the request.user has a notification

    if Notification.objects.filter(receiving_user=request.user).exists():
        notify = Notification.objects.get(receiving_user=request.user)
        flag = True


    # to create a new room during acceptance of pairing/invite
    if request.method == "POST":
        if request.POST["yes"]:

            # auto generate random characters 
            data_type = string.digits
            id_length = random.sample(data_type, 5)
            generated_id = "".join(id_length)

            room_id = generated_id
            if Notification.objects.filter(receiving_user=request.user).exists():

                notify = Notification.objects.get(receiving_user=request.user)
                new_room = Room.objects.create(room_id=room_id, player1=notify.sending_user, player2=notify.receiving_user)
                new_room.save()
                
                print(new_room)


    # to redirect users to their rooms
    rooms = Room.objects.all()
    for room in rooms:
        if room.player1 == request.user:
            room_id = room.room_id

            return redirect("core:room", room.room_id)

        elif room.player2 == request.user:
            room_id = room.room_id

            return redirect("core:room", room.room_id)
    
    return render(request, "core/lobby.html", {"users": all_user, "notification": notify, "flag": flag})



def handshake(request, pk):
    potential_player1 = request.user
    potential_player2 = User.objects.get(id=pk)

    if potential_player2.is_active:
        message = f"'{potential_player1.username}' wants to pair with you"
        notify = Notification.objects.create(sending_user=potential_player1, receiving_user=potential_player2, message=message)
        notify.save()

        messages.info(request, "User has received the request")
        return redirect("core:lobby")
    else:
        messages.info(request, "User is not online for pairing")
        return redirect("core:lobby")



def room(request, pk):
    rooms = Room.objects.get(room_id=pk)
    return render(request, "core/room.html", {"room": rooms})
    


def decline_notification(request):
    note = Notification.objects.get(receiving_user=request.user)
    note.delete()

    messages.success(request, "Invite has being declined")
    return redirect("core:lobby")
