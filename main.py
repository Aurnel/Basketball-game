import pygame
import random
import math as m

pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 600

# Display screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Basketball game')

# function to load image
def load_image(filename, size):
    try:
        img = pygame.image.load(filename)
        return pygame.transform.scale(img, size)
    except:
        pygame.error()
        print(f"{filename} does not exist in the working directory")

court = load_image('Court.png', (WIDTH, HEIGHT))

class player:
    def __init__(self, x, y, file):
        self.x = x
        self.y = y
        self.origx = x
        self.origy = y
        self.file = file
        self.size = (150, 150)
        self.speed = 0
        self.has_ball = False
    def draw(self):
        try:
            img = pygame.image.load(self.file)
            img = pygame.transform.scale(img, self.size)
            screen.blit(img, (self.x, self.y))
            # Draw hitbox for debug
            pygame.draw.rect(screen, (0, 255, 0), self.get_hitbox(), 2)
        except:
            pygame.error()
            print(f"{self.file} does not exist in the working directory")

    def get_hitbox(self):
        return pygame.Rect(self.x + 40, self.y + 40, self.size[0] - 100, self.size[1] - 70)
    
    def move(self):
        self.x += self.speed 

# Load basketball image
basketball_img = load_image('football.png', (50, 50))
basket_img_left = load_image('basket.png',(140,140))
basket_img_right = basket_img_left
# Basketball class
class Basketball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.origx = x
        self.origy = y
        self.speed = 0  
        self.gravity = 0.8  
        self.bounce_factor = 0.8  
        self.is_dropping = False
        self.is_possessed_1 = False
        self.is_possessed_2 = False
        self.is_shot_1 = False
        self.is_shot_2 = False
        self.shoot_speed = 1
        self.vx = 10  
        self.vy = -30  
        self.gravity = 1 

    def drop(self):
        if self.is_dropping:
            self.y += self.speed
            self.speed += self.gravity  
            if self.y >= HEIGHT - 150:
                if self.is_shot_1 or self.is_shot_2:
                    self.is_shot_1,self.is_shot_2 = False,False
                self.y = HEIGHT - 150  
                self.speed = -self.speed * self.bounce_factor  
                if abs(self.speed) < 1:
                    self.speed = 0
                    self.is_dropping = False  

    def draw(self):
        screen.blit(basketball_img, (self.x, self.y))
        # Draw hitbox for debug
        pygame.draw.rect(screen, (255, 0, 0), self.get_hitbox(), 2)

    def get_hitbox(self):
        return pygame.Rect(self.x , self.y, 50, 50)  # Ball size is 50x50
    
    def move(self):
        if self.is_possessed_1 == True:
            self.x += player1.speed
        if self.is_possessed_2 == True:
            self.x += player2.speed
    def shoot(self):
        if self.is_shot_1:
            if self.x <= 800 and self.x >= 100 and self.y <= HEIGHT -150:
                self.x += self.vx
                self.y -= self.vy
                self.vy += self.gravity
            elif self.y >= HEIGHT - 150:
                self.vy = -30
                self.y = HEIGHT - 300
                self.drop()
            elif self.x >= 800 or self.x <= 100:
                restart(basket_left.score,basket_right.score)


        if self.is_shot_2:
            if self.x <= 800 and self.x >= 100 and self.y <= HEIGHT -150:
                self.x -= self.vx
                self.y += self.vy
                self.vy += self.gravity  # Apply gravity
            elif self.x >= 800 or self.x <= 100:
                restart(basket_left.score,basket_right.score)
            elif self.y >= HEIGHT -150:
                self.vy = -30
                self.y = HEIGHT - 300
                self.drop()

class basket:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.is_score = False
        self.score = 0
    def draw(self):
        screen.blit(basket_img_left,(self.x,self.y))
        pygame.draw.rect(screen,(255,0,0),self.get_hitbox(),2)
    def get_hitbox(self):
        return pygame.Rect(self.x + 60,self.y + 60,30,30)

# Create basketball object and players
basketball_object = Basketball(WIDTH / 2.1, HEIGHT / 4)
player1 = player(WIDTH / 9, HEIGHT / 1.6, 'player1.png')
player2 = player((WIDTH * 3) // 4, HEIGHT / 1.6, 'player2.png')
basket_left = basket(95,180)
basket_right = basket(770,180)
def restart(s1,s2):
    player1.x = player1.origx
    player1.y = player1.origy
    player2.x = player2.origx
    player2.y =  player2.origy
    basketball_object.x = basketball_object.origx
    basketball_object.y = basketball_object.origy
    basketball_object.is_possessed_1,basketball_object.is_possessed_2 = False,False
    basketball_object.is_dropping = False
    basketball_object.is_shot_1,basketball_object.is_shot_2 = False,False

font = pygame.font.Font(None, 50)
def draw_score():
    score_text = font.render(f"Player 1: {basket_left.score} | Player 2: {basket_right.score}", True, (255,255,255))
    screen.blit(score_text, (WIDTH//2 - 100, 20))


running = True
while running:
    screen.blit(court, (0, 0))

    # Move players
    player1.move()
    player2.move()  # If you later add control for player2
    basketball_object.move()
    basketball_object.shoot()
    # Draw players and ball
    player1.draw()
    player2.draw()
    basketball_object.draw()
    basket_left.draw()
    basket_right.draw()
    draw_score()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                basketball_object.is_dropping = True  
                if player1.has_ball:
                    basketball_object.is_possessed_1 = False
                    player1.has_ball = False
                    basketball_object.is_dropping = True
                    basketball_object.speed = -10  # Add initial upward throw effect
                elif player2.has_ball:
                    basketball_object.is_possessed_2 = False
                    player2.has_ball = False
                    basketball_object.is_dropping = True
                    basketball_object.speed = -10
                else:
                    basketball_object.is_dropping = True
            if event.key == pygame.K_a and player1.x >= 50:
                player1.speed = -5
            elif event.key == pygame.K_a:
                player1.speed = 0
            if event.key == pygame.K_d and player1.x <= 750:
                player1.speed = 5
            elif event.key == pygame.K_d:
                player1.speed = 0
            if event.key == pygame.K_LEFT and player2.x >=50:
                player2.speed = -5
            elif event.key == pygame.K_LEFT:
                player2.speed = 0
            if event.key == pygame.K_RIGHT and player2.x <=750:
                player2.speed = 5
            elif event.key == pygame.K_RIGHT:
                player2.speed = 0
            if event.key == pygame.K_w:
                basketball_object.is_shot_1 = True
                basketball_object.is_possessed_1 = False
                basketball_object.is_shot_2 = False
                basketball_object.is_possessed_2 = False
            if event.key == pygame.K_UP:
                basketball_object.is_shot_2 = True
                basketball_object.is_possessed_2 = False
                basketball_object.is_shot_1 = False
                basketball_object.is_possessed_1 = False
            if event.key == pygame.K_r:
                restart(basket_left.score,basket_right.score)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d]:
                player1.speed = 0
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player2.speed = 0
    
    basketball_object.drop()  

    # Example collision check:
    if basketball_object.get_hitbox().colliderect(player1.get_hitbox()):
        player1.has_ball = True
        basketball_object.is_possessed_1 = True
        player2.has_ball = False
        basketball_object.is_possessed_2 = False
    elif basketball_object.get_hitbox().colliderect(player2.get_hitbox()):
        player2.has_ball = True
        basketball_object.is_possessed_2 = True
        player1.has_ball = False
        basketball_object.is_possessed_1 = False
    if basketball_object.get_hitbox().colliderect(basket_left.get_hitbox()):
        basket_left.score = 2
        restart(basket_left.score,basket_right.score)
    if basketball_object.get_hitbox().colliderect(basket_right.get_hitbox()):
        basket_left.score = 2
        restart(basket_left.score,basket_right.score)
    

    pygame.display.update()

pygame.quit()
