import pygame as pg
from settings import *


class Wall(pg.sprite.Sprite):
    def __init__(self, walls_group, x, y, w, h):
        pg.sprite.Sprite.__init__(self, walls_group)
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Obstacle(pg.sprite.Sprite):
    def __init__(self, obstacles_group, x, y, w, h):
        pg.sprite.Sprite.__init__(self, obstacles_group)
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
