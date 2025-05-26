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
RED = (255, 50, 50)  # Brighter red
GREEN = (0, 180, 0)  # More vibrant green
BLUE = (30, 30, 60)  # Darker blue background
GOLD = (212, 175, 55)
SILVER = (200, 200, 200)

# Roulette wheel properties
WHEEL_RADIUS = 220  # Slightly larger for better appearance
WHEEL_CENTER = (WIDTH // 2, HEIGHT // 2)
NUM_SLOTS = 37  # 0-36

# Ball properties
BALL_RADIUS = 12  # Slightly larger ball
ball_angle = 0
ball_speed = 0

# Fonts
font = pygame.font.SysFont("Arial", 22, bold=True)  # Better looking font

# Roulette numbers (0-36)
roulette_numbers = list(range(NUM_SLOTS))

# Create enhanced images if they don't exist
if not os.path.exists("enhanced_wheel.png"):
    # Generate enhanced wheel image
    wheel_surf = pygame.Surface((WHEEL_RADIUS*2, WHEEL_RADIUS*2), pygame.SRCALPHA)
    
    # Draw metallic outer ring
    pygame.draw.circle(wheel_surf, SILVER, (WHEEL_RADIUS, WHEEL_RADIUS), WHEEL_RADIUS)
    pygame.draw.circle(wheel_surf, BLACK, (WHEEL_RADIUS, WHEEL_RADIUS), WHEEL_RADIUS-15)
    
    # Draw number pockets with better appearance
    angle_step = 360 / NUM_SLOTS
    for i in range(NUM_SLOTS):
        angle = i * angle_step
        color = RED if i % 2 == 0 else BLACK
        if i == 0:
            color = GREEN
            
        # Draw pocket with bevel effect
        pocket_center_x = WHEEL_RADIUS + math.cos(math.radians(angle + angle_step/2)) * (WHEEL_RADIUS - 30)
        pocket_center_y = WHEEL_RADIUS - math.sin(math.radians(angle + angle_step/2)) * (WHEEL_RADIUS - 30)
        
        # Pocket with 3D effect
        pygame.draw.circle(wheel_surf, color, (int(pocket_center_x), int(pocket_center_y)), 22)
        pygame.draw.circle(wheel_surf, (color[0]//2, color[1]//2, color[2]//2), 
                          (int(pocket_center_x-2), int(pocket_center_y-2)), 20)
        
        # Number text with shadow
        text = font.render(str(roulette_numbers[i]), True, BLACK)
        wheel_surf.blit(text, (pocket_center_x - text.get_width()/2 + 1, 
                             pocket_center_y - text.get_height()/2 + 1))
        text = font.render(str(roulette_numbers[i]), True, WHITE)
        wheel_surf.blit(text, (pocket_center_x - text.get_width()/2, 
                             pocket_center_y - text.get_height()/2))
    
    # Draw center decoration
    pygame.draw.circle(wheel_surf, GOLD, (WHEEL_RADIUS, WHEEL_RADIUS), 30)
    pygame.draw.circle(wheel_surf, BLACK, (WHEEL_RADIUS, WHEEL_RADIUS), 30, 2)
    
    pygame.image.save(wheel_surf, "enhanced_wheel.png")

if not os.path.exists("enhanced_ball.png"):
    # Generate enhanced ball image
    ball_surf = pygame.Surface((BALL_RADIUS*2, BALL_RADIUS*2), pygame.SRCALPHA)
    
    # Draw ball with shine effect
    pygame.draw.circle(ball_surf, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
    pygame.draw.circle(ball_surf, (230, 230, 230), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS-2)
    pygame.draw.circle(ball_surf, (200, 200, 200), (BALL_RADIUS+3, BALL_RADIUS-3), BALL_RADIUS//3)
    
    pygame.image.save(ball_surf, "enhanced_ball.png")

# Load enhanced images
wheel_img = pygame.image.load("enhanced_wheel.png").convert_alpha()
ball_img = pygame.image.load("enhanced_ball.png").convert_alpha()

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

# Main game loop (EXACTLY THE SAME AS BEFORE)
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
        # Make result display match the pocket color
        result_color = WHITE
        if result == 0:
            result_color = GREEN
        elif result % 2 == (0 if result <= 10 or (result >= 19 and result <= 28) else 1):
            result_color = RED
        
        result_text = font.render(f"Result: {result}", True, result_color)
        pygame.draw.rect(screen, BLACK, (10, 10, result_text.get_width()+20, result_text.get_height()+10))
        screen.blit(result_text, (20, 15))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()