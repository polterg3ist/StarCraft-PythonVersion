import pygame
from pygame.sprite import Group
from bullet import Bullet
from enemy import Enemy
from time import time
from player import Player


pygame.init()

DISPLAY_INFO = pygame.display.Info()

WIDTH = DISPLAY_INFO.current_w
HEIGHT = DISPLAY_INFO.current_h

clock = pygame.time.Clock()

start_time_enemy = time()
start_time_shoot = time()

time_wait_for_enemy = 1
time_wait_to_shoot = 0.15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.smoothscale(background_image, (WIDTH, HEIGHT))
background_image_rect = background_image.get_rect()
FPS = 60

player = Player()

bullets = Group()
enemies = Group(Enemy())


def bullets_update():
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.top > screen_rect.bottom:
            bullets.remove(bullet)
        else:
            bullet.draw()
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)


def enemies_update():
    enemies.update()
    for enemy in enemies:
        if enemy.rect.left <= screen_rect.left and enemy.dir_x < 0:
            enemy.dir_x = -enemy.dir_x
        if enemy.rect.bottom >= screen_rect.bottom and enemy.dir_y > 0:
            enemy.dir_y = -enemy.dir_y
        if enemy.rect.right >= screen_rect.right and enemy.dir_x > 0:
            enemy.dir_x = -enemy.dir_x
        if enemy.rect.top <= screen_rect.top and enemy.dir_y < 0:
            enemy.dir_y = -enemy.dir_y
        enemy.draw()

    if pygame.sprite.spritecollideany(player, enemies):
        exit()


def create_enemy():
    global start_time_enemy
    t = time()
    current_time = t - start_time_enemy
    if current_time >= time_wait_for_enemy:
        start_time_enemy = t
        enemies.add(Enemy())


def player_shoot(pos):
    global start_time_shoot
    t = time()
    current_time = t - start_time_shoot
    if current_time >= time_wait_to_shoot:
        start_time_shoot = t
        bullets.add(Bullet(player.rect, pos))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.player_move_left = True
            elif event.key == pygame.K_d:
                player.player_move_right = True
            if event.key == pygame.K_w:
                player.player_move_up = True
            elif event.key == pygame.K_s:
                player.player_move_down = True

            elif event.key == pygame.K_LSHIFT:
                player.player_speed = 10

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.player_move_left = False
            elif event.key == pygame.K_d:
                player.player_move_right = False
            if event.key == pygame.K_w:
                player.player_move_up = False
            elif event.key == pygame.K_s:
                player.player_move_down = False
            elif event.key == pygame.K_LSHIFT:
                player.player_speed = 5

        elif event.type == pygame.MOUSEBUTTONDOWN:
            player_shoot(event.pos)

    screen.blit(background_image, background_image_rect)
    bullets_update()
    player.update()
    player.draw()
    create_enemy()
    enemies_update()

    pygame.display.flip()
    clock.tick(60)
