import pygame as pg
import pygame.sprite
import sys
import math

# global constants
SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = int((SCREEN_WIDTH / 2) / MAP_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS

# global variables
player_x = SCREEN_HEIGHT - SCREEN_HEIGHT/2
player_y = SCREEN_HEIGHT - SCREEN_HEIGHT/2
player_angle = math.pi

# map
MAP = (
    '########'
    '#      #'
    '#    # #'
    '#      #'
    '#      #'
    '#  #   #'
    '#      #'
    '########'
)