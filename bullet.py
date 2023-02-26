from pygame.sprite import Sprite
import math
import pygame


class Bullet(Sprite):
    def __init__(self, plr_rect, pos):
        super(Bullet, self).__init__()
        self.screen = pygame.display.get_surface()
        self.speed = 15
        self.pos = (plr_rect.centerx, plr_rect.centery)
        mx, my = pos
        self.dir = (mx - self.pos[0], my - self.pos[1])
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50, 10))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed,
                    self.pos[1] + self.dir[1] * self.speed)

    def draw(self):
        self.rect = self.image.get_rect(center=self.pos)
        self.screen.blit(self.image, self.rect)