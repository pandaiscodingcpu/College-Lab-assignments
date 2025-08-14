import random

number = random.randint(1,100) # random number generated using the random module from 1 to 100
# basic game rules
print("The number to be guessed is generated....your task it to guess it within 10 chances.\nEach wrong guess will deducted your 10 pts.\nInitially you will have 100 pts")
chance,pts = 1,100 # initial chance is 1 and total pts is 100
print("Start guessing......enter '0' when you want to quit")
while True: # infinite loop for game.
    guess = int(input(f"Chance {chance}: "))
    if chance == 10: # edge case when chance is 10
        pts = pts - 10
        print(f"Sorry no more chances left....\nYour Score was {pts}")
        print(f"The number was {number}")
        break
    if guess == 0: # case for quitting the game in between
        print(f"Exiting....\nYour score was {pts}")
        break
    if guess == number: # case for correct guess
        print(f"Correct guessed!! YOU WON\nYOUR SCORE IS {pts}")
        break
    elif guess!=number:
        # incorrect mitigations for the user
        if guess > number and chance !=10:
            print("Higher value try entering lower value....")
            chance = chance + 1
            pts = pts - 10
            continue
        elif guess < number and chance != 10:
            print("Lower value try entering higher value....")
            chance = chance + 1
            pts = pts - 10
            continue