import pygame as pg
import pygame.sprite
import sys
import math

# global constants
SCREEN_HEIGHT = 480 * 2
SCREEN_WIDTH = SCREEN_HEIGHT
MAP_SIZE = 8
TILE_SIZE = int(SCREEN_HEIGHT / MAP_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
SCALE = SCREEN_HEIGHT / CASTED_RAYS

# global variables
player_x = SCREEN_HEIGHT - SCREEN_HEIGHT/2
player_y = SCREEN_HEIGHT - SCREEN_HEIGHT/2
player_angle = math.pi

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Raycasting")
clock = pg.time.Clock()

#background = pygame.image.load('assets/background.png').convert()
walls = pygame.image.load('assets/walls.png').convert()
textures = {
        'S': walls.subsurface(0, 0, 64, 64),
        'T': walls.subsurface(0, 0, 64, 64),
        'O': walls.subsurface(0, 0, 64, 64),
        'D': walls.subsurface(2 * 64, 2 * 64, 64, 64),
        'W': walls.subsurface(4 * 64, 3 * 64, 64, 64),
        'X': walls.subsurface(0, 2 * 64, 64, 64)}

# map
MAP = list(
    '########'
    '#      #'
    '#  ### #'
    '#    # #'
    '#      #'
    '#  #   #'
    '#  #   #'
    '########'
)