"""Snake, classic arcade game.

Group members:
 - Shulin Lu (SL) - 21188336
 - Amy Liu (AL) - 21190251

Modifications:
1. Increasing snake speed over time
2. Random obstacles on the game field
3. Special fruits with positive/negative effects
4. Start menu with color options and replay functionality

Based on original code from freegames.io
"""

from random import randrange
from turtle import *

from freegames import square, vector

# SL - initial game setup - food position, snake body, and initial direction
food = vector(0, 0) # SL - food starts at coordinates (0,0)
snake = [vector(10, 0)] # SL - snake starts as a single segment at (10,0)
aim = vector(0, -10) # SL - initial direction is downward (0,-10)
obstacles = []  # List to hold obstacle positions
speed = 100 
score = 0
game_over = False

def change(x, y):
    """Change snake direction."""
    # SL - update the aim vector to change the snake's direction
    # SL - called when arrow keys are pressed
    aim.x = x
    aim.y = y

def create_obstacles():
    """Create random obstacles on the field."""
    global obstacles
    obstacles = []

    for _ in range(randrange(4,8)):
        obs = vector(randrange(-15, 15) * 10, randrange(-15, 15) * 10)
        if obs != vector(0,0) and obs != food and obs not in snake:
            obstacles.append(obs)

def inside(head):
    """Return True if head inside boundaries."""
    # SL - check if the snake's head is within the game boundaries, returning flase if head hits wall
    # SL - boundaries are set to -200 to 190 for both x and y coordinates
    if not (-200 < head.x < 190 and -200 < head.y < 190):
        return False
    
    if head in obstacles:
        return False
    
    return True

# SL - main game loop to move the snake
speed = 100  # Initial speed of the snake
score = 0    # Player's score

def move():
    """Move snake forward one segment."""
    global speed, score

    head = snake[-1].copy() # SL - Copy the current head position
    head.move(aim) # SL: move head in current direction

    # SL - Check for game over conditions (hit wall or self)
    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')# SL - draw red square at head position to indicate game over
        update()
        return # SL - End game

    snake.append(head) # SL - Andd new head position to snake body
    #AL : food consumption and growth
    if head == food: # AL : Check if snake's head is at food position
        print('Snake:', len(snake)) # AL : Print current length of the snake
        food.x = randrange(-15, 15) * 10 # AL : Reposition food randomly within boundaries
        food.y = randrange(-15, 15) * 10 

        score += 1  # Increase score
        if score % 3 == 0:
            speed -= 5
            print('Speed increased! Current speed:', speed)

    else:
        snake.pop(0) # AL : Remove tail segment if no food eaten

    # AL : clears screen and redraws snake and food
    clear() # AL : Clear the screen for redrawing

    # AL : Draw each segment of the snake
    for body in snake:
        square(body.x, body.y, 9, 'black')

    # AL : Draw the food
    square(food.x, food.y, 9, 'green') # AL : Draw food as green square
    for: obs in obstacles:
        square(obs.x, obs.y, 9, 'gray') # Draw obstacles as gray squares
        
    update() # AL : Update the screen with new drawings
    
    ontimer(move, speed)


# AL: Game initialization and control setup
setup(420, 420, 370, 0) # AL : Set up the game window size and position
hideturtle() # AL : Hide the turtle cursor
tracer(False) # AL : Turn off automatic screen updates
listen() # AL : Set up to listen for keyboard input

# AL : Bind arrow keys to change snake direction
onkey(lambda: change(10, 0), 'Right') # AL : Right arrow key
onkey(lambda: change(-10, 0), 'Left') # AL : Left arrow key
onkey(lambda: change(0, 10), 'Up') # AL : Up arrow key
onkey(lambda: change(0, -10), 'Down') # AL : Down arrow key

# AL : Start the game loop
move() # AL : Call move function to start the game
done() # Al: keep the window open until closed by the user
