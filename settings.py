import pygame as pg
import pygame.sprite
import sys
import math

# global constants s
SCREEN_HEIGHT = 480 * 2
SCREEN_WIDTH = SCREEN_HEIGHT
MAP_SIZE = 8
TILE_SIZE = 120 # SCREEN_HEIGHT / MAP_SIZE
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
SCALE = SCREEN_HEIGHT / CASTED_RAYS
CENTRAL_RAY = int(SCREEN_WIDTH / 2) - 1

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

# map
MAP = (
    '11111111'
    '10110001'
    '10000111'
    '11100001'
    '10000101'
    '10011101'
    '10000101'
    '11111111'
)

textures = {
    '1': pg.image.load('Assets/textures/1.png').convert(),
    '2': pg.image.load('Assets/textures/2.png').convert(),
    '3': pg.image.load('Assets/textures/3.png').convert()
}

enemy = pg.image.load('Assets/enemy.png').convert_alpha()

sprites = [
    {'image': enemy.subsurface(0, 0, 64, 64), 'x': 600, 'y': 600, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 150, 'y': 500, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 270, 'y': 700, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 250, 'y': 720, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 850, 'y': 400, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 850, 'y': 600, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 550, 'y': 750, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 850, 'y': 750, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 550, 'y': 940, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 850, 'y': 940, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 1050, 'y': 1100, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 1050, 'y': 1300, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 1250, 'y': 1100, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 1250, 'y': 1300, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 700, 'y': 1200, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 700, 'y':1300, 'shift':  0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 600, 'y': 1200, 'shift': 0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    # {'image': enemy.subsurface(0, 0, 64, 64), 'x': 600, 'y':1300, 'shift':  0.4, 'scale': 1.0, 'type': 'soldier', 'dead': False},
    ]

soldier_death = [enemy.subsurface(frame * 64, 5 * 64, 64, 64) for frame in range(1,5)]
soldier_death_count = 0

weapon = {
    'default': pg.image.load('Assets/gun_0.png').convert_alpha(),
    'shot': [
        pg.image.load('Assets/gun_0.png').convert_alpha(),
        pg.image.load('Assets/gun_1.png').convert_alpha(),
        pg.image.load('Assets/gun_2.png').convert_alpha(),
    ],
    'shot_count': 0,
    'animation': False
}

