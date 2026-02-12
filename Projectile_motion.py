import pygame

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 600))
running = True

# Load and scale the ball image
ballimg = pygame.image.load('football.png')
ballimg = pygame.transform.scale(ballimg, (50, 50))

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 5  # Initial horizontal velocity
        self.vy = -20  # Initial vertical velocity (jump)
        self.gravity = 1  # Gravity strength
        self.active = False  # Whether the ball is moving or not

    def draw(self):
        screen.blit(ballimg, (self.x, self.y))

    def move(self):
        if self.active:
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity  # Apply gravity

            # Collision with the ground
            if self.y + 50 >= 600:  # Ground level check
                self.y = 600 - 50  # Keep ball above ground
                self.vy = -self.vy * 0.7  # Simulate bounce with some energy loss

# Create ball object
ball_obj = Ball(100, 500)

while running: 
    screen.fill((255, 255, 255))  # Clear screen
    ball_obj.draw()  # Draw ball
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_obj.active = True  # Start movement

    ball_obj.move()  # Update ball position

    pygame.display.update()
    clock.tick(30)  # Increase FPS for smoother movement

pygame.quit()
