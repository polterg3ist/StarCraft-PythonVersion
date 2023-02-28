import pygame
from pygame.sprite import Group
from enemy import Enemy
from time import time
from player import Player


pygame.init()

DISPLAY_INFO = pygame.display.Info()

WIDTH = DISPLAY_INFO.current_w
HEIGHT = DISPLAY_INFO.current_h

clock = pygame.time.Clock()

start_time_enemy = time()

time_wait_for_enemy = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.smoothscale(background_image, (WIDTH, HEIGHT))
background_image_rect = background_image.get_rect()
FPS = 60


enemies = Group(Enemy())
bullets = Group()

player = Player(bullets, enemies)


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
        player.is_dead = True


def create_enemy():
    global start_time_enemy
    t = time()
    current_time = t - start_time_enemy
    if current_time >= time_wait_for_enemy:
        start_time_enemy = t
        enemies.add(Enemy())


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.player_move_left = True
            elif event.key == pygame.K_d:
                player.player_move_right = True
            if event.key == pygame.K_w:
                player.player_move_up = True
            elif event.key == pygame.K_s:
                player.player_move_down = True
            elif event.key == pygame.K_LSHIFT:
                player.player_speed *= 2
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
            elif event.key == pygame.K_ESCAPE:
                exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot(event.pos)
    screen.blit(background_image, background_image_rect)
    bullets_update()
    player.update()
    create_enemy()
    enemies_update()

    pygame.display.flip()
    clock.tick(60)
