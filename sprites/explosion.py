import pygame as pg
from settings import *
from pygame.math import Vector2


class Explosion(pg.sprite.Sprite):

    def __init__(self, groups, pos) -> None:
        self.groups = groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.image = pg.image.load(EXPLOSION_IMAGE)
        self.image = pg.transform.scale(self.image, (0.2 * SPRITE_BOX, 0.2 * SPRITE_BOX))
        self.rect = self.image.get_rect()
        self.pos = Vector2(pos)
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
    
    def update(self):
        if pg.time.get_ticks() - self.spawn_time > EXPLOSION_LIFETIME:
            self.kill()