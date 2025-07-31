import pygame
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Driving Game")

# Lanes and constants
lanes = [140, 270, 450, 600]
player_y = HEIGHT - 140
clock = pygame.time.Clock()

# Load assets
road = pygame.transform.scale(pygame.image.load("assests/background/road.png"), (WIDTH, HEIGHT))
player_car = pygame.transform.scale(pygame.image.load("assests/cars/player_car.png"), (60, 120))
enemy_car_img = pygame.transform.scale(pygame.image.load("assests/cars/enemy_car1.png"), (60, 120))
fuel_can_img = pygame.transform.scale(pygame.image.load("assests/others/fuel_can.png"), (40, 40))

# Sounds
pygame.mixer.init()
pygame.mixer.music.load("assests/sounds/bg_music.wav")
pygame.mixer.music.play(-1)
crash_sound = pygame.mixer.Sound("assests/sounds/crash.wav")

# Variables
player_lane = 2
player_speed = 5
fuel = 100
score = 0
start_time = pygame.time.get_ticks()
gear = 1
boost = False

# One enemy
enemy = {'x': random.choice(lanes), 'y': random.randint(-600, -100)}

# Fuel cans
fuel_cans = [{'x': random.choice(lanes), 'y': random.randint(-800, -300)} for _ in range(2)]

# Fonts
font = pygame.font.SysFont(None, 36)

# Game state
game_over = False

# Functions
def draw_background(scroll_y):
    scroll_y = (scroll_y + 5) % HEIGHT
    win.blit(road, (0, scroll_y - HEIGHT))
    win.blit(road, (0, scroll_y))
    return scroll_y

def draw_hud():
    pygame.draw.rect(win, (255, 255, 255), (10, 10, 150, 20), 2)  # Fuel bar border
    pygame.draw.rect(win, (0, 255, 0), (12, 12, fuel * 1.46, 16))  # Fuel level
    dist = (pygame.time.get_ticks() - start_time) // 1000
    text = font.render(f"Time: {dist}s  Gear: {gear}  Score: {score}", True, (255, 255, 255))
    win.blit(text, (10, 40))

def reset_game():
    global player_lane, fuel, score, gear, enemy, fuel_cans, game_over, start_time
    player_lane = 2
    fuel = 100
    score = 0
    gear = 1
    enemy = {'x': random.choice(lanes), 'y': random.randint(-600, -100)}
    fuel_cans = [{'x': random.choice(lanes), 'y': random.randint(-800, -300)} for _ in range(2)]
    game_over = False
    start_time = pygame.time.get_ticks()
    pygame.mixer.music.play(-1)

# Main loop
scroll_y = 0
run = True
while run:
    clock.tick(60)
    scroll_y = draw_background(scroll_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not game_over:
        keys = pygame.key.get_pressed()

        # Lane movement
        if keys[pygame.K_LEFT] and player_lane > 0:
            player_lane -= 1
            pygame.time.wait(100)
        if keys[pygame.K_RIGHT] and player_lane < len(lanes) - 1:
            player_lane += 1
            pygame.time.wait(100)

        # Gear & Boost
        if keys[pygame.K_UP] and gear < 5:
            gear += 1
            pygame.time.wait(100)
        if keys[pygame.K_DOWN] and gear > 1:
            gear -= 1
            pygame.time.wait(100)
        boost = keys[pygame.K_SPACE]

        # Fuel consumption
        fuel -= 0.1 if not boost else 0.3
        if fuel <= 0:
            game_over = True

        # Move single enemy
        enemy['y'] += (5 + gear)
        if enemy['y'] > HEIGHT:
            enemy['x'] = random.choice(lanes)
            enemy['y'] = random.randint(-600, -100)
            score += 1

        # Move fuel cans
        for can in fuel_cans:
            can['y'] += (4 + gear)
            if can['y'] > HEIGHT:
                can['x'] = random.choice(lanes)
                can['y'] = random.randint(-800, -300)

        # Collision Detection
        player_rect = pygame.Rect(lanes[player_lane], player_y, 60, 120)
        enemy_rect = pygame.Rect(enemy['x'], enemy['y'], 60, 120)
        if player_rect.colliderect(enemy_rect):
            crash_sound.play()
            pygame.mixer.music.stop()
            game_over = True

        for can in fuel_cans:
            can_rect = pygame.Rect(can['x'], can['y'], 40, 40)
            if player_rect.colliderect(can_rect):
                fuel = min(100, fuel + 30)
                can['y'] = HEIGHT + 100  # Move it out

        # Draw all
        win.blit(player_car, (lanes[player_lane], player_y))
        win.blit(enemy_car_img, (enemy['x'], enemy['y']))
        for can in fuel_cans:
            win.blit(fuel_can_img, (can['x'], can['y']))

        draw_hud()
    else:
        over_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
        win.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))
        if pygame.key.get_pressed()[pygame.K_r]:
            reset_game()

    pygame.display.update()

pygame.quit()
