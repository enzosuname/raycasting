# Imports
import pygame as pg
import pygame.sprite
from settings import *
import sys
import math

# Initialize Pygame
pg.init

# Set Base Screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Raycasting")
clock = pg.time.Clock()

# draw the map
def draw_map():
    for row in range(8):
        #loop over map columns
        for col in range(8):
            #calculate square index
            square = row * MAP_SIZE + col

            # draw map in the game window
            pg.draw.rect(
                screen,
                (200, 200, 200) if MAP[square] == '#' else (100, 100, 100),
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
            target_x = (player_x - math.sin(player_angle))

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

    # background
    pg.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    # draw 2D map
    draw_map()

    # apply raycasting
    cast_rays()

    pg.display.flip()

    clock.tick(30)