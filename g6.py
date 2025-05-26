import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roulette Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (0, 180, 0)
BLUE = (30, 30, 60)
GOLD = (212, 175, 55)
SILVER = (200, 200, 200)

# Roulette wheel properties
WHEEL_RADIUS = 220
WHEEL_CENTER = (WIDTH // 2, HEIGHT // 2)

# European roulette sequence
EUROPEAN_SEQUENCE = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]
NUM_SLOTS = len(EUROPEAN_SEQUENCE)

# Ball properties
BALL_RADIUS = 12
ball_angle = 0
ball_speed = 0

# Fonts
font = pygame.font.SysFont("Arial", 22, bold=True)

# Create enhanced images if they don't exist
if not os.path.exists("european_wheel.png"):
    # Generate wheel image code here (same as before)
    pass

if not os.path.exists("enhanced_ball.png"):
    # Generate ball image code here (same as before)
    pass

# Load images
wheel_img = pygame.image.load("european_wheel.png").convert_alpha()
ball_img = pygame.image.load("enhanced_ball.png").convert_alpha()

def draw_wheel():
    screen.blit(wheel_img, (WHEEL_CENTER[0] - WHEEL_RADIUS, WHEEL_CENTER[1] - WHEEL_RADIUS))

def draw_ball():
    x = WHEEL_CENTER[0] + math.cos(math.radians(ball_angle)) * (WHEEL_RADIUS - BALL_RADIUS - 10)
    y = WHEEL_CENTER[1] - math.sin(math.radians(ball_angle)) * (WHEEL_RADIUS - BALL_RADIUS - 10)
    screen.blit(ball_img, (x - BALL_RADIUS, y - BALL_RADIUS))

def spin_wheel():
    global ball_angle, ball_speed, result
    ball_speed = random.uniform(10, 20)
    ball_angle = random.uniform(0, 360)
    result = None  # Reset result when spinning

# Main game loop
running = True
spinning = False
result = None
last_result = None

while running:
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not spinning:
                spinning = True
                spin_wheel()

    if spinning:
        ball_angle += ball_speed
        ball_speed *= 0.99
        if ball_speed < 0.1:
            spinning = False
            winning_index = int((ball_angle % 360) / (360 / NUM_SLOTS))
            result = EUROPEAN_SEQUENCE[winning_index]
            last_result = result  # Store the last result
            print(f"The ball landed on: {result}")

    draw_wheel()
    draw_ball()

    # Only show result when not spinning and we have a result
    if not spinning and result is not None:
        result_index = EUROPEAN_SEQUENCE.index(result)
        result_color = GREEN if result == 0 else RED if result_index % 2 == 1 else BLACK
        
        # Create text and background
        result_text = font.render(f"Result: {result}", True, result_color)
        text_width = result_text.get_width()
        text_height = result_text.get_height()
        
        # Draw background
        pygame.draw.rect(screen, WHITE, (10, 10, text_width + 20, text_height + 10))
        # Draw text
        screen.blit(result_text, (20, 15))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()