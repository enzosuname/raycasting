# Imports
import pygame as pg
import pygame.sprite
from settings import *
import sys
import math

# draw the map


# raycasting algorithm
past_time = pg.time.get_ticks()

def cast_rays():
    current_time = pg.time.get_ticks()
    current_angle = player_angle + HALF_FOV
    start_angle = player_angle - HALF_FOV
    texture_y = '2'; texture_x = '2'


    for ray in range(CASTED_RAYS):
        current_sin = math.sin(current_angle); current_sin = current_sin if current_sin else 0.000001
        current_cos = math.cos(current_angle); current_cos = current_cos if current_cos else 0.000001
        target_x, direction_x = (SCREEN_WIDTH / 2 + MAP_SCALE, 1) if current_sin >= 0 else (SCREEN_WIDTH / 2, 1)
        # cast ray step by step
        for depth in range(MAX_DEPTH):

            vertical_depth = (target_x - player_x) / current_sin
            horizontal_depth = (target_x - player_x) / current_cos
            target_y = player_y + vertical_depth * current_cos



            # get ray in target coords
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            map_x = int(target_x / MAP_SCALE)
            map_y = int(target_y / MAP_SCALE)
            target_square = map_y * MAP_SIZE + map_x
            # if target_square not in range(len(MAP)): break
            # if MAP[target_square] not in ' e':
            #     texture_y = MAP[target_square] if MAP[target_square] !=

            # convert target Y coord to map row
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            # calculate map square index
            square = row * MAP_SIZE + col
            texture_offset_y = target_y
            texture_offset_x = target_x

            if MAP[square] != '0':
                #pygame.draw.rect(screen, (0, 255, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))


                # draw casted ray
                # pg.draw.line(screen, (0, 255, 0), (player_x, player_y),
                #                (target_x, target_y))

                color = 255/(1 + depth * depth * 0.0001)
                depth *= math.cos(player_angle - start_angle)

                # calc wall height
                wall_height =  MAP_SCALE * 300 / (depth + 0.0001)

                if wall_height > 50000: wall_height = 50000

                # draw 3d projection
                texture_offset = texture_offset_x
                texture = texture_y if vertical_depth < horizontal_depth else texture_x
                depth = vertical_depth if vertical_depth < horizontal_depth else horizontal_depth
                depth *= math.cos(player_angle - current_angle)

                wall_block = textures[texture].subsurface(
                    (texture_offset - int(texture_offset / MAP_SCALE) * MAP_SCALE), 0, 1, 64)
                wall_block = pygame.transform.scale(wall_block, (10, abs(int(wall_height))))
                zbuffer.append(
                    {'image': wall_block, 'x': ray * SCALE, 'y': int(SCREEN_HEIGHT / 2 - wall_height / 2), 'distance': depth})


                # pg.draw.rect(screen, (color, color, color),
                #              (ray * SCALE,
                #               (SCREEN_HEIGHT / 2) - wall_height / 2,
                #               SCALE, wall_height))

                break

        start_angle += STEP_ANGLE

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

    zbuffer = []

    # apply raycasting
    cast_rays()

    zbuffer = sorted(zbuffer, key=lambda k:['distance'], reverse=True)
    for item in zbuffer:
        screen.blit(item['image'], (item['x'], item['y']))

    if keys[pg.K_m]:
        # background
        pg.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

        # draw 2D map
        draw_map()

    clock.tick(30)

    pg.display.flip()

