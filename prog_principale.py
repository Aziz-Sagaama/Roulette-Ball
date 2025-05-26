
import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Roulette - 3 Number Bets")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (0, 200, 0)
BLUE = (30, 30, 60)
GOLD = (255, 215, 0)

# Fonts
font = pygame.font.SysFont("Arial", 22, bold=True)
large_font = pygame.font.SysFont("Arial", 36, bold=True)

# Game variables
WHEEL_RADIUS = 220
WHEEL_CENTER = (WIDTH // 2, HEIGHT // 2)
BALL_RADIUS = 12
ball_angle = 0
ball_speed = 0
spinning = False
result = None
message = ""
message_timer = 0

# Phases
phase = "SETUP"  # SETUP, INPUT_NAMES, GAME, RESULT
num_players_input = ""
players = []
current_player = 0

# European roulette sequence
EUROPEAN_SEQUENCE = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]
NUM_SLOTS = len(EUROPEAN_SEQUENCE)

# Draw roulette wheel
def draw_wheel():
    pygame.draw.circle(screen, BLACK, WHEEL_CENTER, WHEEL_RADIUS)
    for i in range(NUM_SLOTS):
        angle = 360 / NUM_SLOTS * i
        x = WHEEL_CENTER[0] + math.cos(math.radians(angle)) * (WHEEL_RADIUS - 30)
        y = WHEEL_CENTER[1] - math.sin(math.radians(angle)) * (WHEEL_RADIUS - 30)
        number = EUROPEAN_SEQUENCE[i]
        color = GREEN if number == 0 else RED if i % 2 else WHITE
        text = font.render(str(number), True, color)
        screen.blit(text, (x - 10, y - 10))

# Draw the ball
def draw_ball():
    x = WHEEL_CENTER[0] + math.cos(math.radians(ball_angle)) * (WHEEL_RADIUS - BALL_RADIUS - 10)
    y = WHEEL_CENTER[1] - math.sin(math.radians(ball_angle)) * (WHEEL_RADIUS - BALL_RADIUS - 10)
    pygame.draw.circle(screen, GOLD, (int(x), int(y)), BALL_RADIUS)

# Spin the ball
def spin_wheel():
    global ball_angle, ball_speed, spinning, result
    ball_speed = random.uniform(10, 20)
    ball_angle = random.uniform(0, 360)
    spinning = True
    result = None

# Check winners
def check_winner():
    winners = []
    for p in players:
        if result in p["bets"]:
            winners.append(p["name"])
    return winners

# Clear game
def reset_game():
    global phase, num_players_input, players, current_player, spinning, result, message
    phase = "SETUP"
    num_players_input = ""
    players = []
    current_player = 0
    spinning = False
    result = None
    message = ""

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
               # --- SETUP Phase: Input number of players ---
            if phase == "SETUP":
                if event.key == pygame.K_RETURN:
                    if num_players_input.isdigit() and int(num_players_input) > 0:
                         # Create empty player data
                        players = [{"name": "", "bets_str": "", "bets": []} for _ in range(int(num_players_input))]
                        phase = "INPUT_NAMES"
                    else:
                        message = "Invalid number"
                        message_timer = 100
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character from input
                    num_players_input = num_players_input[:-1]
                elif event.unicode.isdigit():
                    num_players_input += event.unicode
               # --- INPUT_NAMES Phase: Enter player names and bets --
            elif phase == "INPUT_NAMES":
                if current_player < len(players):
                    p = players[current_player]
                    if event.key == pygame.K_RETURN:
                        try:
                            bet_list = [int(x.strip()) for x in p["bets_str"].split(",")]
                            if p["name"] and all(0 <= b <= 36 for b in bet_list) and len(bet_list) == 3:
                                p["bets"] = bet_list
                                current_player += 1
                            else:
                                message = "Enter 3 numbers between 0–36"
                                message_timer = 100
                        except:
                            message = "Invalid format (e.g., 3,14,29)"
                            message_timer = 100
                    elif event.key == pygame.K_BACKSPACE:
                         # Allow backspace from bets or name
                        if p["bets_str"]:
                            p["bets_str"] = p["bets_str"][:-1]
                        elif p["name"]:
                            p["name"] = p["name"][:-1]
                    elif event.unicode.isalpha() and not p["bets_str"]:
                           # Allow letters in name before betting starts
                        p["name"] += event.unicode
                    elif event.unicode.isdigit() or event.unicode == ",":
                           # Allow numbers and commas in bet input
                        p["bets_str"] += event.unicode
                else:
                    # All players entered, spin the wheel
                    phase = "GAME"
                    spin_wheel()

            elif phase == "RESULT" and event.key == pygame.K_r:
                reset_game()

    # === UI and Game Flow ===
    # --- SETUP Phase: Display prompt to enter number of players ---
    if phase == "SETUP":
        prompt = large_font.render("Enter number of players:", True, WHITE)
        num_text = large_font.render(num_players_input, True, GREEN)
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 50))
        screen.blit(num_text, (WIDTH//2 - num_text.get_width()//2, HEIGHT//2))

    elif phase == "INPUT_NAMES" and current_player < len(players):
        p = players[current_player]
        name_text = font.render(f"Player {current_player+1} Name: {p['name']}", True, WHITE)
        bet_text = font.render(f"3 Numbers (0–36): {p['bets_str']}", True, WHITE)
        screen.blit(name_text, (WIDTH//2 - 200, HEIGHT//2 - 40))
        screen.blit(bet_text, (WIDTH//2 - 200, HEIGHT//2))
# --- INPUT_NAMES Phase: Prompt for name and bets ---
    elif phase == "GAME":
        draw_wheel()
        draw_ball()
        if spinning:
             # Rotate ball and slow down
            ball_angle += ball_speed
            ball_speed *= 0.98
                # Stop spinning when speed is low
            if ball_speed < 0.5:
                spinning = False
                  # Determine winning number
                winning_index = int((ball_angle % 360) / (360 / NUM_SLOTS))
                result = EUROPEAN_SEQUENCE[winning_index]
                  # Check who won
                winners = check_winner()
                if winners:
                    message = f"🎉 Winner(s): {', '.join(winners)}"
                else:
                    message = "No one won. Try again!"
                message_timer = 300
                phase = "RESULT"

    elif phase == "RESULT":
        draw_wheel()
        draw_ball()
        if result is not None:
            result_text = large_font.render(f"Landed on: {result}", True, GREEN)
            screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 50))
        if message:
            color = GREEN if "Winner" in message else RED
            win_text = large_font.render(message, True, color)
            screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2))
            restart_text = font.render("Press 'R' to restart", True, WHITE)
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT - 50))

    if message_timer > 0:
        message_timer -= 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
