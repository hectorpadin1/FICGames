import pygame as pg
from settings import *
from pygame.math import Vector2
from sprites.bullet import Bullet


class AbstractGun():
    
    def __init__(self, bullet_group, ammo, bullet_img, reload_time):
        self.bullet_group = bullet_group
        self.MAX_AMMO = ammo
        self.ammo = ammo
        self.reload_time = reload_time
        self.bullet_img = bullet_img
        self.last_shot = pg.time.get_ticks()
    
    def shoot(self, pos, rot):
        if self.ammo > 0:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                self.ammo -= 1
                Bullet(self.bullet_group, pos, rot, self.bullet_img)
        else:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.reload_time:
                self.ammo = self.MAX_AMMO
