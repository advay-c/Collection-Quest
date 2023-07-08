import pygame
import random
import os
import time

pygame.font.init()

WIDTH, HEIGHT = 640, 720

ground_image = pygame.image.load(os.path.join('gmtk-assets', 'ground_image.png'))

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

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(80)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
        player_x 
    if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
        player_x 

    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    WINDOW.blit(ground_image, (0, 0))
    WINDOW.blit(PLAYER, (0, 0))
    ground.update(2)  # Update the ground position with a scrolling speed of 2
    WINDOW.blit(ground.image, ground.rect)

    pygame.display.update()

pygame.quit()

