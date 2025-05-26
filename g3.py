import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roulette Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
GOLD = (212, 175, 55)
DARK_GREEN = (0, 50, 0)

# Roulette properties
WHEEL_RADIUS = 300
WHEEL_CENTER = (WIDTH // 2, HEIGHT // 2)
BALL_RADIUS = 15

# European roulette number sequence (starts at top and goes clockwise)
EUROPEAN_SEQUENCE = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]
NUM_SLOTS = len(EUROPEAN_SEQUENCE)
SLOT_ANGLE = 360 / NUM_SLOTS

# Ball physics
ball_angle = 0  # In degrees
ball_speed = 0
spinning = False
result = None

# Font
font = pygame.font.SysFont("Arial", 24)

# Create images if they don't exist
if not os.path.exists("wheel.png"):
    # Generate wheel image
    wheel_surf = pygame.Surface((600, 600), pygame.SRCALPHA)
    pygame.draw.circle(wheel_surf, DARK_GREEN, (300, 300), 300)
    pygame.draw.circle(wheel_surf, GOLD, (300, 300), 250)
    
    # Draw numbers
    for i, num in enumerate(EUROPEAN_SEQUENCE):
        angle = math.radians(i * SLOT_ANGLE - 90)  # -90 to start at top
        x = 300 + 270 * math.cos(angle)
        y = 300 + 270 * math.sin(angle)
        
        # Pocket color
        color = GREEN if num == 0 else RED if i % 2 == 1 else BLACK
        pygame.draw.circle(wheel_surf, color, (int(x), int(y)), 20)
        
        # Number text
        text = font.render(str(num), True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        wheel_surf.blit(text, text_rect)
    
    pygame.image.save(wheel_surf, "wheel.png")

if not os.path.exists("ball.png"):
    # Generate ball image
    ball_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(ball_surf, WHITE, (15, 15), 15)
    pygame.draw.circle(ball_surf, GOLD, (15, 15), 12)
    pygame.image.save(ball_surf, "ball.png")

# Load images
wheel_img = pygame.image.load("wheel.png").convert_alpha()
wheel_img = pygame.transform.scale(wheel_img, (WHEEL_RADIUS*2, WHEEL_RADIUS*2))
ball_img = pygame.image.load("ball.png").convert_alpha()
ball_img = pygame.transform.scale(ball_img, (BALL_RADIUS*2, BALL_RADIUS*2))

def draw_wheel():
    screen.blit(wheel_img, (WHEEL_CENTER[0] - WHEEL_RADIUS, WHEEL_CENTER[1] - WHEEL_RADIUS))

def draw_ball():
    # Calculate ball position (offset slightly inward from numbers)
    ball_x = WHEEL_CENTER[0] + math.cos(math.radians(ball_angle)) * (WHEEL_RADIUS * 0.7)
    ball_y = WHEEL_CENTER[1] - math.sin(math.radians(ball_angle)) * (WHEEL_RADIUS * 0.7)
    screen.blit(ball_img, (ball_x - BALL_RADIUS, ball_y - BALL_RADIUS))

def spin_wheel():
    global ball_angle, ball_speed, spinning, result
    ball_speed = random.uniform(10, 15)
    ball_angle = random.uniform(0, 360)
    spinning = True
    result = None

def get_winning_number(angle):
    """Convert ball angle to exact winning number"""
    normalized_angle = (angle + SLOT_ANGLE/2) % 360  # Center in slot
    winning_index = int(normalized_angle // SLOT_ANGLE)
    return EUROPEAN_SEQUENCE[winning_index]

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((50, 50, 50))  # Dark gray background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not spinning:
            spin_wheel()
    
    # Update ball physics
    if spinning:
        ball_angle += ball_speed
        ball_speed *= 0.995  # Friction
        
        if ball_speed < 0.05:
            spinning = False
            result = get_winning_number(ball_angle)
            print(f"Ball landed at {ball_angle%360:.1f}° -> Number {result}")
    
    # Draw everything
    draw_wheel()
    draw_ball()
    
    # Display result
    if result is not None:
        # Determine color
        if result == 0:
            color = GREEN
        elif EUROPEAN_SEQUENCE.index(result) % 2 == 1:  # Red numbers
            color = RED
        else:
            color = BLACK
        
        result_text = font.render(f"Winner: {result}", True, color)
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 50))
    
    # Instructions
    if not spinning:
        instr_text = font.render("Press SPACE to spin", True, WHITE)
        screen.blit(instr_text, (WIDTH//2 - instr_text.get_width()//2, HEIGHT - 50))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()