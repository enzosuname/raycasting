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
CASTED_RAYS = 100
STEP_ANGLE = FOV / CASTED_RAYS
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
SCALE = SCREEN_HEIGHT / CASTED_RAYS

MAP_SCALE = 64
MAP_RANGE = MAP_SIZE * MAP_SCALE
MAP_SPEED = (MAP_SCALE / 2) / 10

# global variables
player_x = SCREEN_HEIGHT / 2
player_y = SCREEN_WIDTH / 2
player_angle = math.pi / 3

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Raycasting")
clock = pg.time.Clock()

#background = pygame.image.load('assets/background.png').convert()
# walls = pygame.image.load('assets/walls.png').convert()
# textures = {
#         'S': walls.subsurface(0, 0, 64, 64),
#         'T': walls.subsurface(0, 0, 64, 64),
#         'O': walls.subsurface(0, 0, 64, 64),
#         'D': walls.subsurface(2 * 64, 2 * 64, 64, 64),
#         'W': walls.subsurface(4 * 64, 3 * 64, 64, 64),
#         'X': walls.subsurface(0, 2 * 64, 64, 64)}

# map
MAP = (
    '11111111'
    '10110001'
    '10000221'
    '12200001'
    '10000101'
    '10022201'
    '10000201'
    '11111111'
)

textures = {
    '1': pg.image.load('assets/textures/1.png').convert(),
    '2': pg.image.load('assets/textures/2.png').convert(),
    '3': pg.image.load('assets/textures/3.png').convert()
}

