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

# Generate and save wheel image (600x600)
def create_wheel_image():
    wheel_surface = pygame.Surface((600, 600), pygame.SRCALPHA)
    
    # Outer green circle
    pygame.draw.circle(wheel_surface, (0, 100, 0), (300, 300), 300)
    
    # Gold inner circle
    pygame.draw.circle(wheel_surface, (212, 175, 55), (300, 300), 250)
    
    # Number pockets (European layout)
    numbers = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
               24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
    
    font = pygame.font.SysFont('Arial', 20)
    for i, num in enumerate(numbers):
        angle = math.radians(i * (360/len(numbers)) - 90)
        x = 300 + 270 * math.cos(angle)
        y = 300 + 270 * math.sin(angle)
        
        # Pocket color
        color = (0, 128, 0) if num == 0 else (255, 0, 0) if i % 2 == 1 else (0, 0, 0)
        pygame.draw.circle(wheel_surface, color, (int(x), int(y)), 20)
        
        # Number text
        text_color = (255, 255, 255)
        text = font.render(str(num), True, text_color)
        text_rect = text.get_rect(center=(x, y))
        wheel_surface.blit(text, text_rect)
    
    pygame.image.save(wheel_surface, "wheel.png")
    return pygame.image.load("wheel.png").convert_alpha()

# Generate and save ball image (30x30)
def create_ball_image():
    ball_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
    
    # White ball with gold highlight
    pygame.draw.circle(ball_surface, (255, 255, 255), (15, 15), 15)
    pygame.draw.circle(ball_surface, (212, 175, 55), (15, 15), 12)
    
    pygame.image.save(ball_surface, "ball.png")
    return pygame.image.load("ball.png").convert_alpha()

# Try to load or create images
try:
    wheel_img = pygame.image.load('wheel.png').convert_alpha()
    wheel_img = pygame.transform.scale(wheel_img, (600, 600))
except:
    wheel_img = create_wheel_image()

try:
    ball_img = pygame.image.load('ball.png').convert_alpha()
    ball_img = pygame.transform.scale(ball_img, (30, 30))
except:
    ball_img = create_ball_image()

# Game variables
WHEEL_RADIUS = 300
WHEEL_CENTER = (WIDTH//2, HEIGHT//2)
ball_angle = 0
ball_speed = 0
spinning = False
result = None

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((50, 50, 50))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not spinning:
            spinning = True
            ball_speed = random.uniform(8, 15)
            result = None
    
    # Draw wheel
    screen.blit(wheel_img, (WHEEL_CENTER[0]-300, WHEEL_CENTER[1]-300))
    
    # Ball physics
    # In your game loop, replace the spinning logic with:
    if spinning:
        ball_angle += ball_speed
        ball_speed *= 0.995
    
        if ball_speed < 0.1:
         
         spinning = False
         # Calculate exact winning slot
         normalized_angle = ball_angle % 360
         slot_size = 360 / 37
         winning_index = int((normalized_angle + slot_size/2) % 360 // slot_size)
        
         european_sequence = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 
                            11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 
                            22, 18, 29, 7, 28, 12, 35, 3, 26]
        
         result = european_sequence[winning_index]
        
         # Debug output to verify
         print(f"Ball Angle: {normalized_angle:.1f}°")
         print(f"Winning Index: {winning_index}")
         print(f"Winning Number: {result}")
    
    # Draw ball
    ball_x = WHEEL_CENTER[0] + math.cos(math.radians(ball_angle)) * 250
    ball_y = WHEEL_CENTER[1] + math.sin(math.radians(ball_angle)) * 250
    screen.blit(ball_img, (ball_x-15, ball_y-15))
    
    # Display result
    if result is not None:
        color = (0, 128, 0) if result == 0 else (255, 0, 0) if result in [32,19,21,25,34,27,36,30,23,5,16,1,14,9,18,7,12,3] else (0, 0, 0)
        font = pygame.font.SysFont('Arial', 36)
        text = font.render(f"Winner: {result}", True, color)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 50))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()