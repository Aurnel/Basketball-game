import pygame
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load assets with error handling
def load_image(filename, size):
    try:
        img = pygame.image.load(filename)
        return pygame.transform.scale(img, size)
    except pygame.error:
        print(f"Error: '{filename}' not found!")
        pygame.quit()
        exit()

# Load images
playerimg = load_image('spaceship.png', (50, 50))
ufo = load_image('ufo (1).png', (50, 50))
bulletimg = load_image('bullet.png', (10, 20))

# Player setup
player_x = WIDTH // 2
player_y = HEIGHT - 80
player_speed = 5
player_change_x = 0

# Enemy setup
enemy_x = random.randint(50, WIDTH - 50)
enemy_y = random.randint(10, 100)
enemy_speed_x = 3
enemy_speed_y = 40  # Move down when bouncing

# Bullets
bullets = []

# Score setup
score = 0
font = pygame.font.Font(None, 36)  # Default font, size 36

class Bullet:
    def __init__(self, x, y):
        self.x = x + (50 // 2) - (10 // 2)  # Center bullet on spaceship
        self.y = y
        self.speed = 8  # Faster bullets

    def move(self):
        self.y -= self.speed  # Move up

    def draw(self):
        screen.blit(bulletimg, (self.x, self.y))  # Use image for bullet

# Collision detection function
def is_collision(bullet_x, bullet_y, enemy_x, enemy_y):
    return enemy_x < bullet_x < enemy_x + 50 and enemy_y < bullet_y < enemy_y + 50

# Draw functions
def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y):
    screen.blit(ufo, (x, y))

def draw_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 100))  # Background color

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change_x = -player_speed
            if event.key == pygame.K_RIGHT:
                player_change_x = player_speed
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_change_x = 0  # Stop movement smoothly

        # Shooting bullets
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullets.append(Bullet(player_x, player_y))

    # Update player position
    player_x += player_change_x
    player_x = max(0, min(WIDTH - 50, player_x))  # Keep player in bounds

    # Update enemy position
    enemy_x += enemy_speed_x
    if enemy_x >= WIDTH - 50 or enemy_x <= 0:
        enemy_speed_x *= -1  # Bounce back
        enemy_y += enemy_speed_y  # Move down when hitting a wall

    # Update bullets and check for collision
    for bullet in bullets[:]:  # Iterate safely over the list
        bullet.move()
        bullet.draw()

        # Check if bullet hits enemy
        if is_collision(bullet.x, bullet.y, enemy_x, enemy_y):
            print("Enemy Hit!")  # Debugging message
            bullets.remove(bullet)  # Remove bullet
            enemy_x = random.randint(50, WIDTH - 50)  # Respawn enemy
            enemy_y = random.randint(10, 100)
            score += 10  # Increase score

        # Remove off-screen bullets
        if bullet.y < 0:
            bullets.remove(bullet)

    # Draw everything
    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    draw_score()  # Display score
    pygame.display.update()

    clock.tick(60)  # Limit FPS

pygame.quit()
