import pygame
import random

# Initialize pygame
pygame.init()

# Screen
WIDTH = 900
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Night Ninja Dash")

# Colors
DARK_BLUE = (10, 10, 40)
MOON = (240, 240, 200)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (220, 50, 50)
GREEN = (50, 220, 50)

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 40)

# Ground
GROUND_Y = 400

# Ninja
ninja_width = 50
ninja_height = 80

ninja = pygame.Rect(100, GROUND_Y - ninja_height,
                    ninja_width, ninja_height)

velocity_y = 0
gravity = 1
jump_power = -18

is_jumping = False
is_sliding = False

score = 0
level = 1

# Obstacles
obstacles = []

obstacle_timer = 0

running = True

while running:

    clock.tick(60)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Jump
            if event.key == pygame.K_SPACE and not is_jumping:
                velocity_y = jump_power
                is_jumping = True

            # Slide
            if event.key == pygame.K_DOWN:
                is_sliding = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                is_sliding = False

    # -------- LEVELS --------

    if score < 20:
        level = 1
        speed = 6

    elif score < 50:
        level = 2
        speed = 8

    else:
        level = 3
        speed = 10

    # -------- JUMP PHYSICS --------

    velocity_y += gravity
    ninja.y += velocity_y

    if ninja.bottom >= GROUND_Y:
        ninja.bottom = GROUND_Y
        velocity_y = 0
        is_jumping = False

    # -------- SLIDE --------

    if is_sliding and not is_jumping:
        ninja.height = 40
        ninja.y = GROUND_Y - 40
    else:
        ninja.height = 80
        ninja.y = min(ninja.y, GROUND_Y - 80)

    # -------- SPAWN OBSTACLES --------

    obstacle_timer += 1

    if obstacle_timer > 70:

        obstacle_timer = 0

        # Ground obstacle
        if random.randint(1, 2) == 1:

            obstacle = pygame.Rect(
                WIDTH,
                GROUND_Y - 50,
                40,
                50
            )

        # Flying enemy
        else:

            obstacle = pygame.Rect(
                WIDTH,
                GROUND_Y - 120,
                50,
                40
            )

        obstacles.append(obstacle)

    # -------- MOVE OBSTACLES --------

    for obstacle in obstacles[:]:

        obstacle.x -= speed

        if obstacle.right < 0:
            obstacles.remove(obstacle)
            score += 1

        if ninja.colliderect(obstacle):
            running = False

    # -------- DRAW --------

    screen.fill(DARK_BLUE)

    # Moon
    pygame.draw.circle(screen, MOON, (750, 100), 50)

    # Stars
    for i in range(30):
        pygame.draw.circle(
            screen,
            WHITE,
            ((i * 31) % WIDTH, (i * 73) % 200),
            2
        )

    # Ground
    pygame.draw.rect(
        screen,
        GRAY,
        (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y)
    )

    # Ninja
    pygame.draw.rect(screen, GREEN, ninja)

    # Obstacles
    for obstacle in obstacles:

        if obstacle.y < GROUND_Y - 60:
            pygame.draw.rect(screen, RED, obstacle)
        else:
            pygame.draw.rect(screen, WHITE, obstacle)

    # Score
    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    level_text = font.render(
        f"Level: {level}",
        True,
        WHITE
    )

    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 60))

    pygame.display.update()

# -------- GAME OVER --------

pygame.quit()

print("Game Over!")
print("Final Score:", score)