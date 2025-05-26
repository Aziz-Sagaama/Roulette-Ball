import pygame
import random
import math

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

# Function to draw the roulette wheel
def draw_wheel():
    angle_step = 360 / NUM_SLOTS
    for i in range(NUM_SLOTS):
        angle = i * angle_step
        color = RED if i % 2 == 0 else BLACK
        if i == 0:
            color = GREEN  # Green for 0
        pygame.draw.arc(screen, color, (WHEEL_CENTER[0] - WHEEL_RADIUS, WHEEL_CENTER[1] - WHEEL_RADIUS, WHEEL_RADIUS * 2, WHEEL_RADIUS * 2), math.radians(angle), math.radians(angle + angle_step), WHEEL_RADIUS)
        text = font.render(str(roulette_numbers[i]), True, WHITE)
        text_rect = text.get_rect(center=(WHEEL_CENTER[0] + math.cos(math.radians(angle + angle_step / 2)) * (WHEEL_RADIUS - 30), WHEEL_CENTER[1] - math.sin(math.radians(angle + angle_step / 2)) * (WHEEL_RADIUS - 30)))
        screen.blit(text, text_rect)

# Function to draw the ball
def draw_ball():
    x = WHEEL_CENTER[0] + math.cos(math.radians(ball_angle)) * (WHEEL_RADIUS - BALL_RADIUS - 10)
    y = WHEEL_CENTER[1] - math.sin(math.radians(ball_angle)) * (WHEEL_RADIUS - BALL_RADIUS - 10)
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), BALL_RADIUS)

# Function to spin the wheel
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
