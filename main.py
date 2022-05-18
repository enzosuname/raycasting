# Imports
import pygame as pg
import pygame.sprite
from settings import *
import sys
import math
from defs import *
from classes import *


# Start running game
running = True
while running:
    keys = pg.key.get_pressed()
    global target_x
    global target_y
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
            # sys.exit(0)
    if keys[pg.K_LEFT]: player_angle -= 0.1
    if keys[pg.K_RIGHT]: player_angle += 0.1
    if keys[pg.K_UP]:
        forward = True
        player_x += -math.sin(player_angle) * 3
        player_y += math.cos(player_angle) * 3
    if keys[pg.K_DOWN]:
        forward = False
        player_x -= -math.sin(player_angle) * 3
        player_y -= math.cos(player_angle) * 3
    if keys[pygame.K_LCTRL]:
        if weapon['animation'] == False: weapon['animation'] = True

    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)

    square = row * MAP_SIZE + col

    if MAP[square] != '0':
        if forward:
            player_x -= -math.sin(player_angle) * 3
            player_y -= math.cos(player_angle) * 3
        else:
            player_x += -math.sin(player_angle) * 3
            player_y += math.cos(player_angle) * 3

    offset_x = math.sin(player_angle) * MAP_SPEED
    offset_y = math.cos(player_angle) * MAP_SPEED

    pg.draw.rect(screen, (100, 100, 100), (0, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pg.draw.rect(screen, (200, 200, 200), (0, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

    zbuffer = []

    # apply raycasting
    cast_rays(zbuffer)

    for sprite in sprites:
        sprite_x = sprite['x'] - player_x
        sprite_y = sprite['y'] - player_y
        sprite_height = 50
        sprite_ray = 50
        sprite_distance = math.sqrt(abs(sprite_x) ** 2 + abs(sprite_y) ** 2)
        sprite_image = pygame.transform.scale(sprite['image'], (int(sprite_height), int(sprite_height)))
        zbuffer.append({'image': sprite_image, 'x': sprite_ray - int(sprite_height / 2),
                        'y': SCREEN_HEIGHT / 2 - 20, 'distance': sprite_distance})

    zbuffer = sorted(zbuffer, key=lambda k:['distance'], reverse=True)
    for item in zbuffer:
        screen.blit(item['image'], (item['x'], item['y']))

    screen.blit(weapon['default'], (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 193))
    if weapon['animation']:
        weapon['animation'] = True
        screen.blit(weapon['shot'][int(weapon['shot_count'] / 5)], (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 193))
        weapon['shot_count'] += 1
        if weapon['shot_count'] >= 15: weapon['shot_count'] = 0; weapon['animation'] = False;
        pg.display.flip

    if keys[pg.K_m]:
        # background
        pg.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

        # draw 2D map
        draw_map()

    clock.tick(30)

    font = pygame.font.SysFont('Ariel', 30)
    fps_surface = font.render('FPS: ' + str(int(clock.get_fps())), False, (255, 0, 0))
    if keys[pygame.K_f]:
        screen.blit(fps_surface, (120, 0))

    pg.display.flip()

