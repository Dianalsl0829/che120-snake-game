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

from random import randrange, choice
from turtle import *
import time
from freegames import square, vector

# SL - Initial game setup - food position, snake body, and initial direction
food = vector(0, 0)  # SL - Food starts at coordinates (0, 0)
snake = [vector(10, 0)]  # SL - Snake starts as a single segment at (10, 0)
aim = vector(0, -10)  # SL - Initial movement direction is downward (0, -10)
obstacles = []  # AL - List to hold obstacle positions
speed = 200  # SL - Initial game speed
score = 0  # SL - Player's score

# Special food system variables
special_food_active = False  # AL - Track if special food is currently active
special_food_type = None  # AL - Type of special food when active
special_food_timer = 0  # AL - Timer for special food duration
special_effect_active = False  # AL - Track if special effect is active
special_effect_end_time = 0  # AL - Time when special effect ends
current_effect = None  # AL - Currently active effect type

# AL - Define special food types with their properties
SPECIAL_FOOD_TYPES = {
    'speed_boost': {
        'color': 'blue',
        'effect': 'Speed Boost',
        'duration': 8  
    },
    'slow_down': {
        'color': 'purple', 
        'effect': 'Slow Down',
        'duration': 10  
    },
    'invincible': {
        'color': 'gold',
        'effect': 'Invincible Mode',
        'duration': 5   
    },
    'double_points': {
        'color': 'pink',
        'effect': 'Double Points',
        'duration': 15  
    }
}


def change(x, y):
    """Change snake direction."""
    # SL - Updates the aim vector to change snake's movement direction
    # SL - Called when arrow keys are pressed to control snake movement
    aim.x = x
    aim.y = y


def create_obstacles():
    """Create random obstacles on the field."""
    global obstacles
    obstacles = []
    
    # AL - Create 4-7 random obstacles
    for _ in range(randrange(4, 8)):
        obstacle = vector(randrange(-15, 15) * 10, randrange(-15, 15) * 10)
        # AL - Ensure obstacle doesn't spawn on snake start, food, or existing obstacles
        if obstacle != vector(0, 0) and obstacle != food and obstacle not in snake:
            obstacles.append(obstacle)


def inside(head):
    """Return True if head inside boundaries."""
    # SL - Checks if snake head is within the game boundaries
    # SL - Returns False if head hits wall (game over condition)
    # AL - Modified to also check for obstacle collisions
    
    # SL - Boundary check: -200 to 190 for both x and y coordinates
    if not (-200 < head.x < 190 and -200 < head.y < 190):
        return False
    
    # AL - Check for obstacle collisions
    if head in obstacles:
        return False
    
    return True


def try_spawn_special_food():
    """Attempt to spawn special food randomly."""
    global special_food_active, special_food_type, special_food_timer
    
    # AL - Only spawn special food if none is currently active
    if not special_food_active:
        # AL - 20% chance to spawn special food (1 in 5)
        if randrange(1, 6) == 1:
            special_food_active = True
            special_food_type = choice(list(SPECIAL_FOOD_TYPES.keys()))
            
            # AL - Set timer for 20-30 seconds (200-300 game cycles)
            special_food_timer = randrange(50, 100)
            print(f"Special food: {SPECIAL_FOOD_TYPES[special_food_type]['effect']}")


def update_special_food_timer():
    """Update special food timer and handle expiration."""
    global special_food_active, special_food_timer
    
    # AL - Decrement timer if special food is active
    if special_food_active:
        special_food_timer -= 1
        # AL - When timer reaches zero, revert to normal food
        if special_food_timer <= 0:
            print("Normal food regenerated")
            special_food_active = False
            # AL - Generate new normal food position
            food.x = randrange(-15, 15) * 10
            food.y = randrange(-15, 15) * 10


def apply_special_effect(effect_type):
    """Apply special food effect to the game."""
    global special_effect_active, special_effect_end_time, current_effect, speed
    
    special_effect_active = True
    current_effect = effect_type
    effect_info = SPECIAL_FOOD_TYPES[effect_type]
    
    # AL - Calculate when the effect should end
    special_effect_end_time = time.time() + effect_info['duration']
    
    print(f"Effect: {effect_info['effect']} ({effect_info['duration']} seconds)")
    
    # AL - Apply immediate effects based on food type
    if effect_type == 'speed_boost':
        speed = speed - 80  # AL - Increase speed significantly
    elif effect_type == 'slow_down':
        speed = speed + 100  # AL - Decrease speed significantly
    elif effect_type == 'double_points':
        # AL - Double points effect handled during scoring
        pass
    # AL - Invincible effect handled in collision detection


def update_special_effects():
    """Update special effects and handle expiration."""
    global special_effect_active, speed, current_effect
    
    # AL - Check if active effect has expired
    if special_effect_active and time.time() >= special_effect_end_time:
        print(f"Effect ended: {SPECIAL_FOOD_TYPES[current_effect]['effect']}")
        
        # AL - Reset speed changes when speed effects expire
        if current_effect == 'speed_boost':
            speed = speed + 80  # AL - Restore original speed
        elif current_effect == 'slow_down':
            speed = speed - 100  # AL - Restore original speed
        
        special_effect_active = False
        current_effect = None


def draw_game():
    """Draw all game elements on the screen."""
    # AL - Clear the screen for redrawing
    clear()
    
    # AL - Draw each segment of the snake
    for body in snake:
        square(body.x, body.y, 9, 'black')
    
    # AL - Draw food (special or normal)
    if special_food_active:
        # AL - Draw special food with its designated color
        food_color = SPECIAL_FOOD_TYPES[special_food_type]['color']
        square(food.x, food.y, 9, food_color)
    else:
        # AL - Draw normal food as green square
        square(food.x, food.y, 9, 'green')
    
    # AL - Draw all obstacles as gray squares
    for obstacle in obstacles:
        square(obstacle.x, obstacle.y, 9, 'gray')
    
    # AL - Update the screen with new drawings
    update()


def move():
    """Move snake forward one segment."""
    global speed, score, special_food_active, food
    
    # SL - Create new head position by copying current head and moving in aim direction
    head = snake[-1].copy()
    head.move(aim)

    # SL - Check for game over conditions (hit wall, self, or obstacles)
    # AL - Modified to allow invincible mode to bypass collision checks
    if not special_effect_active or current_effect != 'invincible':
        if not inside(head) or head in snake:
            # SL - Draw red square at collision point to indicate game over
            square(head.x, head.y, 9, 'red')
            update()
            return  # SL - End game when collision occurs

    # SL - Add new head position to snake body
    snake.append(head)
    
    # AL - Food consumption and growth mechanism
    if head == food:
        points_earned = 1
        
        # AL - Handle special food effects
        if special_food_active:
            apply_special_effect(special_food_type)
            special_food_active = False
            
            # AL - Special food scoring: double points or bonus points
            if current_effect == 'double_points':
                points_earned = points_earned * 2  # AL - Double points for double points effect
            else:
                points_earned = 3  # AL - Bonus points for other special foods
        else:
            # AL - Normal food gives 1 point
            points_earned = 1

        # AL - Update score and print game status
        score += points_earned
        print(f'Snake: {len(snake)} | Score: {score} (+{points_earned})')
        
        # AL - Generate new food position
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10

        # AL - Attempt to spawn special food
        try_spawn_special_food()

        # SL - Speed increase logic: every 3 points increases speed
        if score % 3 == 0 and speed > 50:
            speed -= 20
            print(f'Speed increased! Current speed: {speed}')

    else:
        # AL - Remove tail segment if no food was eaten (snake moves forward)
        snake.pop(0)

    # AL - Update special food and effect timers
    update_special_food_timer()
    update_special_effects()

    # AL - Draw all game elements
    draw_game()
    
    # SL - Schedule next move with current speed
    ontimer(move, speed)


# AL - Game initialization and control setup
setup(420, 420, 370, 0)  # AL - Set up game window size and position
hideturtle()  # AL - Hide the turtle cursor for cleaner display
tracer(False)  # AL - Turn off animation for immediate drawing
listen()  # AL - Listen for keyboard input

# AL - Create initial obstacles
create_obstacles()

# AL - Bind arrow keys to direction change functions
onkey(lambda: change(10, 0), 'Right')   # AL - Right arrow moves right
onkey(lambda: change(-10, 0), 'Left')   # AL - Left arrow moves left
onkey(lambda: change(0, 10), 'Up')      # AL - Up arrow moves up
onkey(lambda: change(0, -10), 'Down')   # AL - Down arrow moves down

# AL - Start the game loop
move()  # AL - Begin the main game movement loop
done()  # AL - Keep window open until manually closed