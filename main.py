# Imports
import pygame as pg
import pygame.sprite
from settings import *
import sys
import math

# draw the map
def draw_map():
    for row in range(8):
        # loop over map columns
        for col in range(8):
            # calculate square index
            square = row * MAP_SIZE + col

            # draw map in the game window
            pg.draw.rect(
                screen,
                (200, 200, 200) if MAP[square] != '0' else (100, 100, 100),
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
            )

    # draw player
    pg.draw.circle(screen, (255, 0, 0), (int(player_x), int(player_y)), 8)

    # direction
    pg.draw.line(screen, (0, 255, 0), (player_x, player_y),
                     (player_x - math.sin(player_angle) * 50,
                      player_y + math.cos(player_angle) * 50), 3)

    # draw player FOV
    pg.draw.line(screen, (0, 255, 0), (player_x, player_y),
                     (player_x - math.sin(player_angle - HALF_FOV) * 50,
                      player_y + math.cos(player_angle - HALF_FOV) * 50), 3)
    pg.draw.line(screen, (0, 255, 0), (player_x, player_y),
                     (player_x - math.sin(player_angle + HALF_FOV) * 50,
                      player_y + math.cos(player_angle + HALF_FOV) * 50), 3)

# raycasting algorithm
def cast_rays():
    start_angle = player_angle - HALF_FOV

    for ray in range(CASTED_RAYS):
        # cast ray step by step
        for depth in range(MAX_DEPTH):
            # get ray in target coords
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            # convert target Y coord to map row
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            # calculate map square index
            square = row * MAP_SIZE + col

            if MAP[square] != '0':
                #pygame.draw.rect(screen, (0, 255, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))


                #draw casted ray
                #pg.draw.line(screen, (0, 255, 0), (player_x, player_y),
                             #(target_x, target_y))

                color = 255/(1 + depth * depth * 0.0001)
                depth *= math.cos(player_angle - start_angle)

                # calc wall height
                wall_height =  21000 / (depth + 0.0001)

                if wall_height > SCREEN_HEIGHT: wall_height = SCREEN_HEIGHT

                # draw 3d projection
                pg.draw.rect(screen, (color, color, color),
                             (ray * SCALE,
                              (SCREEN_HEIGHT / 2) - wall_height / 2,
                              SCALE, wall_height))

                break

        start_angle += STEP_ANGLE

# Start running game
running = True
while running:
    keys = pg.key.get_pressed()
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





    pg.draw.rect(screen, (100, 100, 100), (0, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pg.draw.rect(screen, (200, 200, 200), (0, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

    # apply raycasting
    cast_rays()

    if keys[pg.K_m]:
        # background
        pg.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

        # draw 2D map
        draw_map()

    clock.tick(30)

    pg.display.flip()

