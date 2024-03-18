import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Adventure Leap")

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED=(255,0,0)
# Load the image of Yoshi
yoshi_image = pygame.image.load(r'C:\Users\Administrator\Documents\NDU\NDU SPRING 2024\ENG 202\png-transparent-mario-yoshi-super-mario-world-2-yoshi-s-island-yoshi-nintendo-vertebrate-cartoon-thumbnail.png')
yoshi_image = pygame.transform.scale(yoshi_image, (30, 30))  # Scale the image to the desired size


# Load the background image
background_image = pygame.image.load(r'C:\Users\Administrator\Documents\NDU\NDU SPRING 2024\ENG 202\images.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


# Create the player character
# Modify the Player class to use Yoshi as the character's sprite
# Modify the Player class to set a limit to the ground
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = yoshi_image  # Use the Yoshi image
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.vel_x = 0
        self.vel_y = 0
        self.jump_power = -10
        self.gravity = 0.5
        self.on_ground = False
        self.ground_limit = 10000 # Set the ground limit

    def update(self):
        # Check if the player is below the ground limit
        if self.rect.y > self.ground_limit:
            self.rect.y = self.ground_limit
            self.vel_y = 0
            self.on_ground = True
        else:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y

            # Check for collisions with platforms
            platform_collisions = pygame.sprite.spritecollide(self, platforms, False)
            for platform in platform_collisions:
                if self.vel_y > 0:  # If player is moving down
                    self.rect.bottom = platform.rect.top  # Set player's bottom to platform's top
                    self.vel_y = 0
                    self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

     #create the obstacle object
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(Obstacle, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)  # Fill the obstacle with a color (e.g., RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Create the platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(Platform, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Create the game objects
player = Player()
platforms = pygame.sprite.Group(Platform(0, 500, screen_width, 100))
all_sprites = pygame.sprite.Group(player, platforms)

clock = pygame.time.Clock()
running = True
#create obstacle
obstacles = pygame.sprite.Group()
obstacles.add(Obstacle(300, 450, 50, 50))  # Example obstacle at position (300, 450) with size 50x50


# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.jump()

    # Update player
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player.rect.x -= 5
    if keys[K_RIGHT]:
        player.rect.x += 5

    all_sprites.update()
    obstacles.update()

    # Check for collisions between player and platforms
    if pygame.sprite.spritecollide(player, platforms, False):
        player.rect.y -= player.vel_y
        player.vel_y = 0
        player.on_ground = True

    # Draw background
    screen.blit(background_image, (0, 0))
    obstacles.draw(screen)

    # Draw sprites
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
