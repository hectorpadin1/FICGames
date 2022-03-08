import pygame as pg
from settings import *
from pygame.math import Vector2
from random import uniform
from sprites.explosion import *
from gestorrecursos import GestorRecursos as GR
from soundcontroller import SoundController as SC


class Bullet(pg.sprite.Sprite):
    
    def __init__(self, bullet_group, pos, rot, img):
        pg.sprite.Sprite.__init__(self, bullet_group)
        dir = Vector2(1, 0).rotate(-rot)
        #pos = pos + BARREL_OFFSET.rotate(-rot)
        self.image = GR.load_image(img)
        self.image = pg.transform.rotate(self.image, rot-90)
        self.rect = self.image.get_rect()
        self.pos = Vector2(pos)
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = pos
        #spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        #self.vel = dir.rotate(spread) * BULLET_SPEED
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        SC.play_metralleta()

    def update(self, dt):
        self.pos += self.vel * (dt/1000)
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
    