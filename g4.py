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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Roulette wheel properties
WHEEL_RADIUS = 200
WHEEL_CENTER = (WIDTH // 2, HEIGHT // 2)
NUM_SLOTS = 37  # 0-36

# Ball properties
BALL_RADIUS = 10
ball_angle = 0
ball_speed = 0

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Roulette numbers (0-36)
roulette_numbers = list(range(NUM_SLOTS))

# Create images if they don't exist
if not os.path.exists("roulette_wheel.png"):
    # Generate wheel image
    wheel_surf = pygame.Surface((WHEEL_RADIUS*2, WHEEL_RADIUS*2), pygame.SRCALPHA)
    
    # Draw the wheel with numbers (same logic as draw_wheel())
    angle_step = 360 / NUM_SLOTS
    for i in range(NUM_SLOTS):
        angle = i * angle_step
        color = RED if i % 2 == 0 else BLACK
        if i == 0:
            color = GREEN
        pygame.draw.arc(wheel_surf, color, (0, 0, WHEEL_RADIUS*2, WHEEL_RADIUS*2), 
                       math.radians(angle), math.radians(angle + angle_step), WHEEL_RADIUS)
        text = font.render(str(roulette_numbers[i]), True, WHITE)
        text_rect = text.get_rect(center=(
            WHEEL_RADIUS + math.cos(math.radians(angle + angle_step / 2)) * (WHEEL_RADIUS - 30),
            WHEEL_RADIUS - math.sin(math.radians(angle + angle_step / 2)) * (WHEEL_RADIUS - 30)
        ))
        wheel_surf.blit(text, text_rect)
    
    pygame.image.save(wheel_surf, "roulette_wheel.png")

if not os.path.exists("roulette_ball.png"):
    # Generate ball image
    ball_surf = pygame.Surface((BALL_RADIUS*2, BALL_RADIUS*2), pygame.SRCALPHA)
    pygame.draw.circle(ball_surf, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
    pygame.image.save(ball_surf, "roulette_ball.png")

# Load images
wheel_img = pygame.image.load("roulette_wheel.png").convert_alpha()
ball_img = pygame.image.load("roulette_ball.png").convert_alpha()

def draw_wheel():
    screen.blit(wheel_img, (WHEEL_CENTER[0] - WHEEL_RADIUS, WHEEL_CENTER[1] - WHEEL_RADIUS))

def draw_ball():
    x = WHEEL_CENTER[0] + math.cos(math.radians(ball_angle)) * (WHEEL_RADIUS - BALL_RADIUS - 10)
    y = WHEEL_CENTER[1] - math.sin(math.radians(ball_angle)) * (WHEEL_RADIUS - BALL_RADIUS - 10)
    screen.blit(ball_img, (x - BALL_RADIUS, y - BALL_RADIUS))

def spin_wheel():
    global ball_angle, ball_speed
    ball_speed = random.uniform(10, 20)
    ball_angle = random.uniform(0, 360)

# Main game loop
running = True
spinning = False
result = None

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
        ball_speed *= 0.99  # Slow down the ball
        if ball_speed < 0.1:
            spinning = False
            result = roulette_numbers[int((ball_angle % 360) / (360 / NUM_SLOTS))]
            print(f"The ball landed on: {result}")

    draw_wheel()
    draw_ball()

    if result is not None:
        result_text = font.render(f"Result: {result}", True, WHITE)
        screen.blit(result_text, (10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()