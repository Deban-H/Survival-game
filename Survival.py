import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mind Control Battle")

# Colors
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Player attributes
player_size = 20
player_color = PURPLE
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5

# Monster attributes
monster_size = 60
monster_color = RED
monster_speed = 2

# Trap attributes
trap_color = BLACK
trap_size = 20
n_traps = 10
traps = [[random.randint(0, SCREEN_WIDTH - trap_size), random.randint(0, SCREEN_HEIGHT - trap_size)] for _ in range(n_traps)]

# Number of monsters
n_monsters = 5
monsters = [[random.randint(0, SCREEN_WIDTH - monster_size), random.randint(0, SCREEN_HEIGHT - monster_size)] for _ in range(n_monsters)]

# Game states
game_over = False
start_screen = True

# Instructions
def draw_instructions():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text1 = font.render("Welcome to Survival battle!", True, WHITE)
    text2 = font.render("You are the purple circle.Monsters are red snakes chasing you", True, WHITE)


    text3 = font.render("Avoid traps (black squares) and monsters!", True, WHITE)
    text4 = font.render("Press any key to start the game.", True, WHITE)

    screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(text4, (SCREEN_WIDTH // 2 - text4.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()

# Draw player
def draw_player(player_pos):
    pygame.draw.circle(screen, player_color, player_pos, player_size)

# Draw monsters
def draw_monster(monster_pos):
    pygame.draw.rect(screen, monster_color, (*monster_pos, monster_size, monster_size // 2))

# Draw traps
def draw_trap(trap_pos):
    pygame.draw.rect(screen, trap_color, (*trap_pos, trap_size, trap_size))

# Update monster positions to chase the player
def move_monsters(monsters, player_pos):
    for monster_pos in monsters:
        if monster_pos[0] < player_pos[0]:
            monster_pos[0] += monster_speed
        if monster_pos[0] > player_pos[0]:
            monster_pos[0] -= monster_speed
        if monster_pos[1] < player_pos[1]:
            monster_pos[1] += monster_speed
        if monster_pos[1] > player_pos[1]:
            monster_pos[1] -= monster_speed

# Check for collisions
def check_collision(player_pos, monster_pos):
    return (player_pos[0] - monster_pos[0])**2 + (player_pos[1] - monster_pos[1])**2 < (player_size + monster_size // 2)**2

def check_trap_collision(player_pos, trap_pos):
    return (trap_pos[0] < player_pos[0] < trap_pos[0] + trap_size) and (trap_pos[1] < player_pos[1] < trap_pos[1] + trap_size)

# Game loop
while not game_over:
    if start_screen:
        draw_instructions()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                start_screen = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] - player_speed > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] + player_speed < SCREEN_WIDTH:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] - player_speed > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] + player_speed < SCREEN_HEIGHT:
        player_pos[1] += player_speed

    # Move monsters
    move_monsters(monsters, player_pos)

    # Check for collisions with monsters
    for monster_pos in monsters:
        if check_collision(player_pos, monster_pos):
            game_over = True

    # Check for collisions with traps
    for trap_pos in traps:
        if check_trap_collision(player_pos, trap_pos):
            game_over = True

    # Redraw game elements
    screen.fill(WHITE)
    draw_player(player_pos)
    for monster_pos in monsters:
        draw_monster(monster_pos)
    for trap_pos in traps:
        draw_trap(trap_pos)

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
