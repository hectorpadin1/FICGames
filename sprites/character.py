import pygame as pg
from pygame.math import Vector2

class Character(pg.sprite.Sprite):
    def __init__(self, groups, img, hit_rect, x, y, health):
        super().__init__(groups)
        self.image = img
        self.rect = img.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = hit_rect
        self.hit_rect.center = self.rect.center
        self.vel = Vector2(0, 0)
        self.pos = Vector2(x, y)
        self.rot = 0
        self.health = health
    