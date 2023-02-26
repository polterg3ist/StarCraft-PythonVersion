import pygame
import math
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.original_image = pygame.image.load('player.png').convert_alpha()
        self.original_image = pygame.transform.smoothscale(self.original_image, (100, 100))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.player_speed = 5

        self.player_move_up = False
        self.player_move_down = False
        self.player_move_left = False
        self.player_move_right = False

    def rotate_player(self):
        mx, my = pygame.mouse.get_pos()
        rel_x, rel_y = mx - self.rect.centerx, my - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rotate_player()

        if self.player_move_up and self.rect.top > self.screen_rect.top:
            self.rect.y -= self.player_speed
        elif self.player_move_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.player_speed
        if self.player_move_left and self.rect.left > self.screen_rect.left:
            self.rect.x -= self.player_speed
        elif self.player_move_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.player_speed

    def draw(self):
        self.screen.blit(self.image, self.rect)