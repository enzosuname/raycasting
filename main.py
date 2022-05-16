# Imports
import pygame as pg
import pygame.sprite
from settings import *
import sys
import math

# draw the map a


# raycasting algorithm
global past_time
past_time = pg.time.get_ticks()

def cast_rays():
    global past_time
    current_time = pg.time.get_ticks()
    current_angle = player_angle + HALF_FOV
    start_angle = player_angle - HALF_FOV
    texture_x = '1' ; texture_y = '1'


    if current_time >= past_time + 30:
        past_time = current_time
        global target_x
        global target_y
        for ray in range(CASTED_RAYS):
            current_sin = math.sin(current_angle); current_sin = current_sin if current_sin else 0.000001
            current_cos = math.cos(current_angle); current_cos = current_cos if current_cos else 0.000001
            target_x, direction_x = (SCREEN_WIDTH / 2 + MAP_SCALE, 1) if current_sin >= 0 else (SCREEN_WIDTH / 2, 1)
            # cast ray step by step
            for depth in range(MAX_DEPTH):

                vertical_depth = (target_x - player_x) / current_sin
                horizontal_depth = (target_x - player_x) / current_cos

                # get ray in target coords
                target_x = player_x - math.sin(start_angle) * depth
                target_y = player_y + math.cos(start_angle) * depth

                map_x = int(target_x / MAP_SCALE)
                map_y = int(target_y / MAP_SCALE)
                target_square = map_y * MAP_SIZE + map_x
                # texture_y = MAP[target_square]
                # if target_square not in range(len(MAP)): break
                # if MAP[target_square] not in ' e':
                #     texture_y = MAP[target_square] if MAP[target_square] !=

                # convert target Y coord to map row
                col = int(target_x / TILE_SIZE)
                row = int(target_y / TILE_SIZE)

                # calculate map square index
                square = row * MAP_SIZE + col
                texture_offset_y = target_y - 20
                texture_offset_x = target_x - 20

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
                    texture_offset = texture_offset_y #if vertical_depth < horizontal_depth else texture_offset_x
                    texture = texture_y if vertical_depth < horizontal_depth else texture_x
                    depth = vertical_depth if vertical_depth < horizontal_depth else horizontal_depth
                    depth *= math.cos(player_angle - current_angle)

                    wall_block = textures[texture].subsurface(
                        (texture_offset - int(texture_offset / MAP_SCALE) * MAP_SCALE), 0, 1, 64)
                    wall_block = pygame.transform.scale(wall_block, (10, abs(int(wall_height))))
                    zbuffer.append(
                        {'image': wall_block,
                         'x': ray * SCALE,
                         'y': int(SCREEN_HEIGHT / 2 - wall_height/2),
                         'distance': depth})


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

    for sprite in sprites:
        if sprite['type'] == 'soldier' and not sprite['dead']:
            pygame.draw.circle(screen, (0, 0, 255),
                               (int((sprite['x'] / MAP_SCALE) * 5), int((sprite['y'] / MAP_SCALE) * 5)), 2)

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
    cast_rays()

    for sprite in sprites:
        sprite_x = sprite['x'] - player_x
        sprite_y = sprite['y'] - player_y
        sprite_distance = math.sqrt(sprite_x * sprite_x + sprite_y * sprite_y)
        sprite2player_angle = math.atan2(sprite_x, sprite_y)
        player2sprite_angle = sprite2player_angle - player_angle
        if sprite_x < 0: player2sprite_angle += math.pi * 2
        if sprite_x > 0 and math.degrees(player2sprite_angle) <= -180: player2sprite_angle += math.pi * 2
        if sprite_x < 0 and math.degrees(player2sprite_angle) >= 180: player2sprite_angle -= math.pi * 2
        shift_rays = player2sprite_angle / STEP_ANGLE
        sprite_ray = CENTRAL_RAY - shift_rays
        if sprite['type'] == 'soldier' and sprite['dead'] == True:
            sprite_height = min(sprite['scale'] * MAP_SCALE * 300 / (sprite_distance + 0.0001), 400)
        else: sprite_height = sprite['scale'] * MAP_SCALE * 300 / (sprite_distance + 0.0001)
        if sprite['type'] == 'soldier':
            if not sprite['dead']:
                if abs(shift_rays) < 20 and sprite_distance < 500 and weapon['animation']:
                    sprite['image'] = soldier_death[int(soldier_death_count / 8)]
                    soldier_death_count += 1
                    if soldier_death_count >= 16: sprite['dead'] = True; soldier_death_count = 0
            else: sprite['image'] = soldier_death[-1]
            if weapon['shot_count'] > 16 and sprite['image'] in [soldier_death[0], soldier_death[1], soldier_death[2]]:
                try:
                    sprite['image'] = soldier_death[int(soldier_death_count / 8) + 2]
                except:
                    pass
                soldier_death_count += 1
                if soldier_death_count >= 32: sprite['dead'] = True; soldier_death_count = 0
            if not sprite['dead'] and sprite_distance <= 10: player_x -= offset_x; player_y -= offset_y
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

