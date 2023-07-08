import pygame
import random
import os
import time

pygame.font.init()

WIDTH, HEIGHT = 640, 720
GRAVITY = 0.01

ground_image = pygame.image.load(os.path.join('gmtk-assets', 'ground_image.png'))
PLAYER = pygame.image.load(os.path.join('imgs', 'bird.png'))

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GMTK-2023")

ground_height = ground_image.get_height()
player_height = PLAYER.get_height()

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

player_x = WIDTH // 2 - PLAYER.get_width() // 2
player_y = HEIGHT // 2 - player_height // 2
player_vel = 5

def gravity():
    global player_y
    player_y += GRAVITY

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(80)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
        player_y -= player_vel
    if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
        player_y += player_vel
    if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
        player_x -= player_vel
    if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
        player_x += player_vel

    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    WINDOW.blit(ground_image, (0, 0))
    gravity()  # Apply gravity to the player
    WINDOW.blit(PLAYER, (player_x, player_y))
    ground.update(2)  # Update the ground position with a scrolling speed of 2
    WINDOW.blit(ground.image, ground.rect)

    pygame.display.update()

pygame.quit()

