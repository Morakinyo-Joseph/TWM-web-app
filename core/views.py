from django.shortcuts import render, redirect
from .models import User, Room, Notification
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import string
import random
import json
from .forms import BoardPlacementForm, WhitePieceForm, BlackPieceForm


# Create your views here.


def landing_page(request):

    # dropping users in their rooms
    rooms = Room.objects.all()
    for room in rooms:
        if room.player1 == request.user:
            room_id = room.room_id

            return redirect("core:room", room_id)

        elif room.player2 == request.user:
            room_id = room.room_id

            return redirect("core:room", room_id)

    return render(request, "core/landing_page.html")


def create(request):

    # dropping users in their rooms
    rooms = Room.objects.all()
    for room in rooms:
        if room.player1 == request.user:
            room_id = room.room_id

            return redirect("core:room", room_id)

        elif room.player2 == request.user:
            room_id = room.room_id

            return redirect("core:room", room_id)


    # get the selected user name
    if request.method == "POST":
        username = request.POST["user"]
        password = "password"
        email = "email@email.com"

        User.objects.create_user(username=username, first_name="firstname", last_name="lastname", password=password, email=email)

        the_user = authenticate(username=username, password=password)
        login(request, the_user)

        return redirect("core:lobby")

    return render(request, "core/create-user.html")


@login_required
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
                

    # dropping users in their rooms
    rooms = Room.objects.all()
    for room in rooms:

        if room.player1 == request.user:
            room_id = room.room_id

            if room.available == False:
                print(f"room {room.id} has being deleted")
                room.delete()
                return redirect("core:lobby")

            return redirect("core:room", room_id)
            

        elif room.player2 == request.user:
            room_id = room.room_id

            if room.available == False:
                print(f"room {room.id} has being deleted")
                room.delete()
                return redirect("core:lobby")

            return redirect("core:room", room_id)


    return render(request, "core/lobby.html", {"users": all_user, "notification": notify, "flag": flag})


def handshake(request, pk):
    # a request to pair
    
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


def move_piece(request, post, piece, room):

    post = post - 1 #to be accurate on the exact post

    try:
        with open(f"core/gameboards/game_board{room.player1}_{room.player2}.json") as f:
            data = json.load(f)

            counter = 0 # looping to see if
            counter2 = 0 #

            available = False #checks wether a piece already exists on board

            for j in data["board"]:
                old_post = data["board"][counter]
                new_post = data["board"][post]

                if old_post["piece"] == piece:
                    available = True
                    break

                counter += 1


            if available:
                for i in data["board"]:
                    old_post = data["board"][counter]
                    new_post = data["board"][post]

                    if new_post["filled"] == False:

                        if old_post["piece"] == piece:
                            if old_post["filled"] == True:

                                old_post["piece"] = None
                                old_post["filled"] = False

                                new_post["piece"] = piece
                                new_post["filled"] = True

                                with open(f'core/gameboards/game_board{room.player1}_{room.player2}.json', 'w') as f:
                                    json.dump(data, f, indent=2)

                                    messages.info(request, "Piece moved correctly")
                                    return piece
                    else:
                        messages.info(request, "Can't move there!")
                        break

                    counter2 += 1
                    

            elif available == False:
                for k in data["board"]:
                    new_post = data["board"][post]

                    if new_post["filled"] == False:
                        new_post["piece"] = piece
                        new_post["filled"] = True
                        with open(f'core/gameboards/game_board{room.player1}_{room.player2}.json', 'w') as f:
                            json.dump(data, f, indent=2)
                            
                            messages.info(request, "Piece moved correctly")
                            return piece
                    else:
                        messages.info(request, "Can't move there!")
                        break 

    except FileNotFoundError:
        with open("core/gameboards/game_board.json") as f:
            data = json.load(f)

            counter = 0 # 
            counter2 = 0 #

            available = False #checks wether a piece already exists on board

            for j in data["board"]:
                old_post = data["board"][counter]
                new_post = data["board"][post]

                if old_post["piece"] == piece:
                    available = True
                    break

                counter += 1


            if available:
                for i in data["board"]:
                    old_post = data["board"][counter]
                    new_post = data["board"][post]

                    if new_post["filled"] == False:

                        if old_post["piece"] == piece:
                            if old_post["filled"] == True:

                                old_post["piece"] = None
                                old_post["filled"] = False

                                new_post["piece"] = piece
                                new_post["filled"] = True

                                with open(f'core/gameboards/game_board{room.player1}_{room.player2}.json', 'w') as f:
                                    json.dump(data, f, indent=2)

                                    messages.info(request, "Piece moved correctly")
                                    return piece
                    else:
                        messages.info(request, "Can't move there!")
                        break

                    counter2 += 1
                    

            elif available == False:
                for k in data["board"]:
                    new_post = data["board"][post]

                    if new_post["filled"] == False:
                        new_post["piece"] = piece
                        new_post["filled"] = True
                        with open(f'core/gameboards/game_board{room.player1}_{room.player2}.json', 'w') as f:
                            json.dump(data, f, indent=2)

                            messages.info(request, "Piece moved correctly")
                            return piece
                    else:
                        messages.info(request, "Can't move there!")
                        break



def room(request, pk):
    rooms = Room.objects.get(room_id=pk)

    board_post = BoardPlacementForm()
    white_piece = WhitePieceForm()
    black_piece = BlackPieceForm()

    if request.method == "POST":
        board_post = BoardPlacementForm(request.POST)
        white_piece = WhitePieceForm(request.POST)
        black_piece = BlackPieceForm(request.POST)

        if request.POST.get("piece"):
            the_post = request.POST["post"]
            the_piece = request.POST["piece"]

            print(f"\nPlaced '{the_piece}' at {the_post}\n")
            
            result = move_piece(request, post=int(the_post), piece=the_piece, room=rooms)
            print(result)


    player1 = rooms.player1
    player2 = rooms.player2

    player1_piece = []
    player2_piece = []

    # verifying if the opponent is still in the game
    if player1 == player2:
        messages.info(request, "Opponent has left the game")
        rooms.available = False
        rooms.save()
        return redirect("core:lobby")
    elif player2 == player1:
        messages.info(request, "Opponent has left the game")
        rooms.available = False
        rooms.save()
        return redirect("core:lobby")


    tracker = {} #this will serve as my context for html rendering

    counter = 0
    board_list = []

    try:
        with open(f'core/gameboards/game_board{rooms.player1}_{rooms.player2}.json') as f:
            data = json.load(f)
            for i in data["board"]:
                board = {
                    "post": data["board"][counter]["post"],
                    "piece": data["board"][counter]["piece"],
                    "filled": data["board"][counter]["filled"]
                }
                board_list.append(board)
                counter += 1

    except FileNotFoundError:
        with open('core/gameboards/game_board.json') as f:
            data = json.load(f)
            for i in data["board"]:
                board = {
                    "post": data["board"][counter]["post"],
                    "piece": data["board"][counter]["piece"],
                    "filled": data["board"][counter]["filled"]
                }
                board_list.append(board)
                counter += 1

    tracker = {
        "board": board_list,
        "room": rooms,
        "board_post": board_post,
        "player1Piece": player1_piece,
        "player2Piece": player2_piece,
        "white_piece": white_piece,
        "black_piece": black_piece,
    }


    return render(request, "core/room.html", tracker)
    

def decline_notification(request):
    note = Notification.objects.get(receiving_user=request.user)
    note.delete()

    messages.success(request, "Invite has being declined")
    return redirect("core:lobby")


def leave(request):
    rooms  = Room.objects.all()
    the_user = request.user

    for room in rooms:
        if room.player1 == the_user:
            room.player1 = room.player2 #making the opponent become both the player 1 and 2
            room.save()

        elif room.player2 == the_user:
            room.player2 = room.player1 #making the opponent become both the player 1 and 2
            room.save()

    logout(request)

    the_user.delete()
    return redirect("core:create-user")