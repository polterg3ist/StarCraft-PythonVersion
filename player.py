import pygame
import math
from pygame.sprite import Sprite
from time import time
from bullet import Bullet


class Player(Sprite):
    def __init__(self, bullets, enemies):
        super(Player, self).__init__()
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.original_image = pygame.image.load('player.png').convert_alpha()
        self.original_image = pygame.transform.smoothscale(self.original_image, (100, 100))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.player_speed = 5
        self.shoot_cooldown = 0.1
        self.shoot_start_time = time()
        self.is_dead = False
        self.bullets = bullets
        self.enemies = enemies

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

    def shoot(self, pos):
        if not self.is_dead:
            t = time()
            current_time = t - self.shoot_start_time
            if current_time >= self.shoot_cooldown:
                self.shoot_start_time = t
                self.bullets.add(Bullet(self.rect, pos))

    def death(self):
        self.bullets.empty()
        self.enemies.empty()
        font = pygame.font.SysFont("TimesNewRoman", 45)

        text1 = font.render("You are dead!", True, (255, 255, 100), (0, 0, 0))
        place1 = self.screen_rect.center
        rect1 = text1.get_rect(center=place1)

        text2 = font.render("Press ESC to quit the game", True, (0, 255, 0), (0, 0, 0))
        place2 = (rect1.centerx, rect1.bottom+30)
        rect2 = text2.get_rect(center=place2)

        self.screen.blit(text1, rect1)
        self.screen.blit(text2, rect2)

    def update(self):
        if self.is_dead:
            self.death()
        else:
            self.rotate_player()
            if self.player_move_up and self.rect.top > self.screen_rect.top:
                self.rect.y -= self.player_speed
            elif self.player_move_down and self.rect.bottom < self.screen_rect.bottom:
                self.rect.y += self.player_speed
            if self.player_move_left and self.rect.left > self.screen_rect.left:
                self.rect.x -= self.player_speed
            elif self.player_move_right and self.rect.right < self.screen_rect.right:
                self.rect.x += self.player_speed
            self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)