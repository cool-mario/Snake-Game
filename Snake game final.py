# Write your code here :-)
# Write your code here :-)
"""
# Filename: Snake game in python
# Author:   Aidan Chan =D
# Date:     Feb 1, 2022 - Feb 3
#
# hello viewer!
# here are some cool features to try:
    • If you die, press p to reset!!!  (the reset took soo long to make)
    • press r to leave your body behind and start a new snake
    • Actually playable (at least on my computer)
    • Press esc key to pause the game!!!! (This also took a while to implement)
    • if you go to the edge of the screen, you will be teleported back to the middle
    • Snake head becomes purple colored when you hit yourself, showing that you died
    • Everytime you eat food, you get a compliment
    • Snake can go to Infinite length!! (well, until you fill the screen)
    • Score and snake length indicator in the top left
"""

"""Imports"""
from tkinter import *
from tkinter import Tk, Canvas
from tkinter import messagebox  # nice unused lol
import time, copy, random
import threading

"""Gobal Variables"""
screen_width = 600  # The window height and width in pixels
screen_height = 600

screen_rows = 15  # how much real estate you give the snake
screen_cols = 15

cell_size = (screen_width/screen_rows)/2.3  # size of each square

displayLabel = ""  # Label to display score and other stuff
winLoseLabel = ""   # the label in the middle that shows game over or something

firstTime = False   # shows whether this is the first time that you run the game

"""Functions"""
def updateScreen():
    global gridCanvases, gridStates, screen_rows, screen_cols, cell_size, gridStates, snakeHead, snakeLength, snakeBody, firstTime, snakeSpeed, foodAmount, foodLocations, display, pause, winLoseLabel, displayLabel, winLosePlaying, invincible, root   # global every single variable for no reason

    deepCopySnakeHead = copy.deepcopy(snakeHead)
    snakeBody.append(deepCopySnakeHead)            # save the past location of the snake head so it can become the body
    gridStates[deepCopySnakeHead[0]][deepCopySnakeHead[1]] = 3

    if len(snakeBody) > snakeLength: # if snake too long, delete its butt lol
        try:
            gridCanvases[snakeBody[0][0]][snakeBody[0][1]].destroy()  # try and except for spam protection
        except:
            print("Error: Tried to destroy butt but is didn't exist for some reason")

        snakeBody.remove(snakeBody[0]) # remove the first item in the list, which is the butt

    #print(snakeBody)
    #print(snakeHead)
    if not pause and not invincible:    # only if you're playing the game should you check for collisions
        if snakeHead in snakeBody[0:len(snakeBody)-1]:  # if you smash into yourself, you lose!
            #print("SnakeBody:",snakeBody)
            #print("SnakeHead:",snakeHead)
            if snakeHead in snakeBody:
                pause = True
                winLosePlaying = "lose"


    if snakeHead in foodLocations:  # if the coord of hte head is inside food, it must have eaten it duh
        move_food(snakeHead)
        snakeLength += 1

    gridStates[snakeHead[0]][snakeHead[1]] = 2

    for i in range(screen_rows):
        for j in range(screen_cols):
            cellColor = "gray"  # the defualt color of the cell, no longer used

            if gridStates[i][j] == 1:  # the food apple
                #cellColor = "firebrick1"
                cellColor = "red"

            elif gridStates[i][j] == 2:  # the snake head
                if winLosePlaying == "lose":
                    cellColor = "purple"
                else:
                    cellColor = "springgreen4"

            elif [i,j] in snakeBody:     # the snake body
                cellColor = "green3"
            #grid[i].append()
            # create canvas
            if cellColor != "gray":
                if firstTime == True:
                    print("firstTime detected",i," ",j)
                    gridCanvases[i][j] = Canvas(root, width=cell_size, height=cell_size, bg=cellColor, border=10, highlightthickness=0, relief='flat')
                    gridCanvases[i][j].place(relx=i/screen_rows, rely=j/screen_cols, anchor=NW)
                else:
                    try:
                        gridCanvases[i][j].configure(bg=cellColor)
                    except:  # if the cell has been deleted by the snake
                        gridCanvases[i][j] = Canvas(root, width=cell_size, height=cell_size, bg=cellColor, border=10, highlightthickness=0, relief='flat')
                        try:
                            gridCanvases[i][j].place(relx=i/screen_rows, rely=j/screen_cols, anchor=NW)  # Spam protection 2 levels
                        except:
                            gridCanvases[i][j] = Canvas(root, width=cell_size, height=cell_size, bg=cellColor, border=10)
                            gridCanvases[i][j].place(relx=i/screen_rows, rely=j/screen_cols, anchor=NW)
                    firstTime == False

    #print("win lose label:",winLoseLabel)
    if winLosePlaying == "win":             # change the win/Lose label state
        winLoseLabel.configure(text="You win!!")
        winLoseLabel.place(relx=0.4, rely=0.4, anchor=NW)
    elif winLosePlaying == "lose":
        winLoseLabel.configure(text="You lose!!\npress p to reset", width=15)
        winLoseLabel.place(relx=0.3, rely=0.3, anchor=NW)
        winLoseLabel.tkraise()
    elif winLosePlaying == "playing":
        winLoseLabel.place(relx=1, rely=1, anchor=NW)



def resetGame():
    global winLosePlaying, pause, snakeBody, snakeHead, snakeFacing, score, snakeLength, snakeSpeed, gridCanvases, gridStates, screen_cols, screen_rows, foodLocations, foodAmount, firstTime, displayLabel, winLoseLabel, invincible

    if not firstTime:
        destroyScreen(root)  # DESTROY!!!!!!!!!!!!!!!!! only if there is already something in the grid

    winLoseLabel = Label(root, text="Loading...", height=2, width=10)
    winLoseLabel.configure(background='turquoise1')
    winLoseLabel.configure(font=("Courier new", 25))
    winLoseLabel.configure(foreground='black')
    winLoseLabel.place(relx=0.4, rely=0.4, anchor=NW)

    gridStates = []  # grid with the numbers, 0 = nothing, 1 = food, 2 = snake
    gridCanvases = []

    for i in range(screen_rows): # make the grids for the first time
        gridStates.append([])
        gridCanvases.append([])
        for j in range(screen_cols):
            gridStates[i].append(0)
            gridCanvases[i].append(0)

    # Everything about the snake:

    snakeHead = [screen_rows // 2, screen_cols // 2]  # the head of the snake, in the center of the screen
    snakeBody = []  # list of coordinates for every part of the snakeBody
    snakeFacing = "right"  # where the snake is facing
    snakeLength = 2  # snake starting length
    snakeSpeed = 0.15

    # Everything about food:
    foodLocations = []
    foodAmount = 3
    for i in range(foodAmount):
        foodLocations.append([random.randint(0, screen_rows - 1), random.randint(0, screen_cols - 1)])  # add random food bits

    for i in foodLocations:
        gridStates[i[0]][i[1]] = 1  # place food one the grid

    firstTime = True   # for creating the canvases for the first time
    pause = False
    score = 0          # the score is how much food you have eaten
    winLosePlaying = "playing"   # shows
    invincible = False      # check for collisons

    displayLabel = Label(root, text="Score: " + str(score) + "\nLength: " + str(snakeLength), height=3, width=10)
    displayLabel.configure(background='black')
    displayLabel.configure(font=("Courier new", 25))
    displayLabel.configure(foreground='white')
    displayLabel.place(relx=0.05, rely=0.05, anchor=NW)

    print("game RESET!!!!!")




def key_pressed(event):
    global snakeHead, snakeBody, snakeLength, snakeFacing, pause, winLosePlaying

    if event.char == "c":
        resetGame()  # just for debugging

    if pause == True and event.char == "p":  # p to reset the game
        resetGame()

    #print("Key Pressed:", event.char)
    if len(event.char) > 0:
        x = ord(event.char)
    #print("key number:", x)
    if x == 27:                   # pause the game!!!!! no way!!!
        pause = not pause
        invincible = True
        print("toggle paused:", pause)
    if pause:
        return

    if event.char == "r":         # leave your body behind....
        snakeLength = 1
        snakeBody.clear()

    if event.char == "w" or x == 63232:
        if snakeFacing != "up" and snakeFacing != "down":
            gridStates[snakeHead[0]][snakeHead[1]] = 0
            snakeFacing = "up"
            snakeHead[1] -= 1
        else:
            return
    elif event.char == "s" or x == 63233:
        if snakeFacing != "down" and snakeFacing != "up":
            gridStates[snakeHead[0]][snakeHead[1]] = 0
            snakeFacing = "down"
            snakeHead[1] += 1
        else:
            return
    elif event.char == "a" or x == 63234:
        if snakeFacing != "left" and snakeFacing != "right":
            gridStates[snakeHead[0]][snakeHead[1]] = 0
            snakeFacing = "left"
            snakeHead[0] -= 1
        else:
            return
    elif event.char == "d" or x == 63235:
        if snakeFacing != "right" and snakeFacing != "left":
            gridStates[snakeHead[0]][snakeHead[1]] = 0
            snakeFacing = "right"
            snakeHead[0] += 1
        else:
            return

    try:
        gridStates[snakeHead[0]][snakeHead[1]] = 2
    except:
        snakeHead = [screen_rows//2, screen_cols//2]
        gridStates[snakeHead[0]][snakeHead[1]] = 2

    if event.char == "w" or event.char == "a" or event.char == "s" or event.char == "d" or x == 63232 or x == 63233 or x == 63234 or x == 63235: # fixes a glitch so that you don't die when pressing any other key
        updateScreen()

def all_children(window): # returns everything in the frame
    children = window.winfo_children()
    for item in children :
        if item.winfo_children():
            children.extend(item.winfo_children())
    return children
def destroyScreen(window):
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()

def move_food(eatenFoodCoords):
    global foodAmount, foodLocations, gridStates, snakeBody, snakeHead, snakeLength, score

    foodLocations.remove(eatenFoodCoords)  # delete food
    gridStates[eatenFoodCoords[0]][eatenFoodCoords[1]] = 0 ############################

    while True:
        randX = random.randint(0,screen_rows-1)
        randY = random.randint(0,screen_cols-1)
        if not([randX,randY] in snakeBody or [randX,randY] in foodLocations):
            break                               # break if valid location

    foodLocations.append([randX,randY])
    gridStates[randX][randY] = 1

    score += 1   # increase the score
    print("SCORE:",score)
    print("LENGTH:",snakeLength,"\n")

    displayLabel.configure(text="Score: " + str(score) + "\nLength: " + str(snakeLength))  # you only need to change the label when you eat food, so
    print(compliments[random.randint(0,len(compliments)-1)])   #???



def move_snake():
    global snakeFacing, gridStates, snakeHead, firstTime, snakeSpeed, pause, compliments
    while True:
        while not pause:
            time.sleep(snakeSpeed)  # move the snake
            #print("SnakeFacing: " + snakeFacing)
            gridStates[snakeHead[0]][snakeHead[1]] = 0
            if snakeFacing == "up":
                snakeHead[1] -= 1

            elif snakeFacing == "down":
                snakeHead[1] += 1

            elif snakeFacing == "left":
                snakeHead[0] -= 1

            elif snakeFacing == "right":
                snakeHead[0] += 1

            try:
                gridStates[snakeHead[0]][snakeHead[1]] = 2
            except:
                snakeHead = [screen_rows//2, screen_cols//2]
                gridStates[snakeHead[0]][snakeHead[1]] = 2
            updateScreen()

            if firstTime == True:
                firstTime = False



"""Begin here"""
def init():
    print("Starting Snake Game, made by Aidan Chan!!")

    resetGame() # reset the game at the beginning?!?!?

    global root, screen_width, screen_height, screen_cols, screen_rows, root, root, displayLabel, winLoseLabel

    x = threading.Thread(target=move_snake, daemon=True)  # what deamon?
    x.start()                                             # start thread


    #updateScreen()
    #firstTime = False

    gridStates[snakeHead[0]][snakeHead[1]] = 2   # place head for the first time
    for i in gridStates:
        print(i)

    # Capture keystrokes here. The keys will never escape...
    root.bind("<Key>", key_pressed)
    # This runs forever, waiting for mouse clicks. What is it waiting for?
    root.mainloop()


# root should be global and used by all functions so it's out here now
root = Tk()
root.geometry(str(screen_width) + "x" + str(screen_height))
root.title("Snake game by AIDAN CHAN")
root.configure(background='black')
compliments = ["🅰🅸🅳🅰🅽 🅲🅷🅰🅽", "🄰🄸🄳🄰🄽 🄲🄷🄰🄽", "Ⓐⓘⓓⓐⓝ Ⓒⓗⓐⓝ", "𝐀𝐢𝐝𝐚𝐧 𝐂𝐡𝐚𝐧", "ᗩIᗪᗩᑎ ᑕᕼᗩᑎ", "𝔸𝕚𝕕𝕒𝕟 ℂ𝕙𝕒𝕟", "Noice.", "Yo you ate a red square!", "good job!", "Apple!", "heckin' good!", "fancy!"] # Aidan Chan?

init()

"""
Known glitches: shhhhhh we don't talk about these
    Rarely the snake leaves behind a body part, I have no clue why
    sometimes, resetting after losing leaves a dark green square in the middle
    sometimes, resetting after losing make the food not dissapear.
    Fixed!! pause doesn't work unless invincible mode is on
    Fixed!! pressing any key except for the normal keys instanly lose the game
"""
