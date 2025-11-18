"""Snake, classic arcade game.

Group members:
 - Shulin Lu (SL) - 21188336
 - Amy Liu (AL) - 21190251

Exercises
1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to mouse clicks.
"""

from random import randrange
from turtle import *

from freegames import square, vector

# SL - initial game setup - food position, snake body, and initial direction
food = vector(0, 0) # SL - food starts at coordinates (0,0)
snake = [vector(10, 0)] # SL - snake starts as a single segment at (10,0)
aim = vector(0, -10) # SL - initial direction is downward (0,-10)


def change(x, y):
    """Change snake direction."""
    # SL - update the aim vector to change the snake's direction
    # SL - called when arrow keys are pressed
    aim.x = x
    aim.y = y


def inside(head):
    """Return True if head inside boundaries."""
    # SL - check if the snake's head is within the game boundaries, returning flase if head hits wall
    # SL - boundaries are set to -200 to 190 for both x and y coordinates
    return -200 < head.x < 190 and -200 < head.y < 190

# SL - main game loop to move the snake
def move():
    """Move snake forward one segment."""
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, 'black')

    square(food.x, food.y, 9, 'green')
    update()
    ontimer(move, 100)


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
move()
done()
