from pygame.sprite import  Sprite
from random import randint
import pygame


class Enemy(Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("meteorite.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (120, 80))
        self.rect = self.image.get_rect()
        self.rect.bottom = self.screen_rect.top
        self.rect.centerx = randint(0, self.screen_rect.width)
        self.speed = 10
        self.dir_x = randint(-5, 5)
        self.dir_y = self.speed

    def update(self):
        self.rect.x += self.dir_x
        self.rect.y += self.dir_y

    def draw(self):
        self.screen.blit(self.image, self.rect)
