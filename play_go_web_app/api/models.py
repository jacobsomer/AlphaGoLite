from django.db import models
import string
import random


def generate_unique_code():
    length = 6
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break
    return code


def pickRandomColor():
    return random.choice(["#6200EE", "#018786", "#B00020", "#FFDE03", "#0336FF", "#FF0266"])


def randomNameP2():
    while True:
        player2Suggestion = 'Anonymous ' + random.choice(["Duck", "Tuna", "Koala",
                                                          "Giraffe", "Armadillo", "Bear",
                                                          "Cheetah", "Penguin", "Whale", "Serpent"]) + random.choice([str(x) for x in range(100)])
        if Room.objects.filter(player1=player2Suggestion).count() == 0:
            return player2Suggestion


def randomNameP1():
    while True:
        player1Suggestion = 'Anonymous ' + random.choice(["Duck", "Tuna", "Koala",
                                                          "Giraffe", "Armadillo", "Bear",
                                                          "Cheetah", "Penguin", "Whale", "Serpent"]) + random.choice([str(x) for x in range(100)])
        try:
            tmp=Room.objects.filter(player2=player1Suggestion).count()
        except:
            tmp=Room.objects.filter(player1=player1Suggestion).count()
        if tmp == 0:
            return player1Suggestion


class Room(models.Model):
    code = models.CharField(
        max_length=8, default=generate_unique_code, unique=True)

    host = models.CharField(max_length=50, unique=True)

    # user names of the players
    player1 = models.CharField(
        default=randomNameP1, max_length=50, unique=True)
    player2 = models.CharField(
        default=randomNameP2, max_length=50, unique=True)

    # stored as hex codes
    player1Color = models.CharField(max_length=7, default=pickRandomColor)
    player2Color = models.CharField(max_length=7, default=pickRandomColor)

    # store the number of people in a room
    num_spectators = models.IntegerField(default=0, null=False)

    # turn == True ==> player 1 is going
    # turn == False ==> player 2 is going
    turn = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # state i.e. 2d array to store the go board
    # we must use a charfield which then must be converted
    # from JavaScript String -> Python list
    # and then,
    # from Python string -> JavaScript array
    board = models.CharField(max_length=765, unique=False, default="[]")

    # spectators
    spectatorArray = models.CharField(
        max_length=275, unique=False, default="[]")
    """
    Home Page
       /  \
    Room   Create Room Page
    Join            |
    Page           /
        \         / 
          \      /
            Room ---------------Direct link to Room
        Objects     
            Board=[]
            Turn?
            Player1/AI? and color
            Player2/AI? and color
            Spectators=[]  
    """
