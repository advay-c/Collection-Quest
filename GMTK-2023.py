import pygame
import random
import os
import time

pygame.font.init()

WIDTH, HEIGHT = 640, 720
PLAYER_HEIGHT = 130
PLAYER_WIDTH = 130
BORDER = pygame.Rect(0, 0, WIDTH, HEIGHT)

ground_image = pygame.image.load(os.path.join('gmtk-assets', 'ground_image.png'))
PLAYER = pygame.image.load(os.path.join('gmtk-assets', 'coin.png'))
PLAYER = pygame.transform.scale(PLAYER, (PLAYER_HEIGHT, PLAYER_WIDTH))
game_over_text = pygame.image.load(os.path.join('gmtk-assets', 'gameover.png'))
restart = pygame.image.load(os.path.join('gmtk-assets', 'restart.png'))

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GMTK-2023")

ground_height = ground_image.get_height()

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ground_image.get_width(), ground_height * 2))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.image.blit(ground_image, (0, 0))
        self.image.blit(ground_image, (0, ground_height))

    def update(self, vel):
        self.rect.y -= vel  # Increase the scrolling speed
        if self.rect.y <= -ground_height:
            self.rect.y = 0

ground = Ground(0, 0)

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

button = Button(WIDTH // 2 - 65, HEIGHT // 2 - 15, restart)

player_x = 250
player_y = 250
gravity = 2
game_over = False

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(80)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()

    if not game_over:
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            player_x -= 5  # Move the player position to the left

        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            player_x += 5  # Move the player position to the right

        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            player_y -= 7

        player_y += gravity  # Apply constant downward displacement to the player's vertical position

        # Check if the player has touched the ground and reset the vertical position
        if player_y >= HEIGHT - PLAYER_HEIGHT:
            game_over = True
            player_y = HEIGHT - PLAYER_HEIGHT

        # Check for collision with the border
        if player_x < BORDER.left:
            player_x = BORDER.left
            game_over = True
        elif player_x > BORDER.right - PLAYER_WIDTH:
            player_x = BORDER.right - PLAYER_WIDTH
            game_over = True
        if player_y < BORDER.top:
            player_y = BORDER.top
            game_over = True
        elif player_y > BORDER.bottom - PLAYER_HEIGHT:
            player_y = BORDER.bottom - PLAYER_HEIGHT
            game_over = True

    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    WINDOW.blit(ground_image, (0, 0))
    ground.update(2)  # Update the ground position with a scrolling speed of 2
    WINDOW.blit(ground.image, ground.rect)
    pygame.draw.rect(WINDOW, (255, 255, 255), BORDER, 1)  # Draw the border
    WINDOW.blit(PLAYER, (player_x, player_y))

    if game_over:
        WINDOW.blit(game_over_text, (200, 200))
        button.draw(WINDOW)

        if button.is_clicked():
            game_over = False
            player_x = 250
            player_y = 250

    pygame.display.update()

pygame.quit()
