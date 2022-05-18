import pygame as pg
import pygame.sprite
from settings import *
import sys
import math
from defs import *


class Player:
    def __init__(self):
        player_pos = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
        self.x, self.y = player_pos
        self.angle = player_angle
        self.sensitivity = 0.004

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()
        if keys[pygame.K_w]:
            nx = self.x + player_speed * cos_a
            ny = self.y + player_speed * sin_a
            self.check_collision(nx, ny)
        if keys[pygame.K_s]:
            nx = self.x + -player_speed * cos_a
            ny = self.y + -player_speed * sin_a
            self.check_collision(nx, ny)
        if keys[pygame.K_a]:
            nx = self.x + player_speed * sin_a
            ny = self.y + -player_speed * cos_a
            self.check_collision(nx, ny)
        if keys[pygame.K_d]:
            nx = self.x + -player_speed * sin_a
            ny = self.y + player_speed * cos_a
            self.check_collision(nx, ny)
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02