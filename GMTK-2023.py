import pygame
import random
import os

pygame.font.init()

WIDTH, HEIGHT = 640, 720

START = pygame.image.load(os.path.join('gmtk-assets', 'START.jpg')) #load images
ground_image = pygame.image.load(os.path.join('gmtk-assets', 'ground_image.jpg'))

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GMTK-2023")

ground_width = ground_image.get_width()

running = True
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    WINDOW.blit(ground_image, (0, 0)) #placing image on screen
    WINDOW.blit(START, (0, 360))
    pygame.display.update()

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ground_width * 2, ground_image.get_height()))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.image.blit(ground_image, (0, 0))
        self.image.blit(ground_image, (ground_width, 0))

    def update(self):
        if self.rect.x <= -ground_width:
            self.rect.x = 0

pygame.quit()
