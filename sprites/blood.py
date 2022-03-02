import pygame as pg
from settings import *
from pygame.math import Vector2
from gestorrecursos import GestorRecursos as GR

class Blood(pg.sprite.Sprite):

    def __init__(self, groups, pos, sx, sy, rot) -> None:
        self.groups = groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.image = GR.load_image(GR.BLOOD_IMAGE)
        self.image = pg.transform.scale(self.image, (sx * SPRITE_BOX, sy * SPRITE_BOX))
        self.image = pg.transform.rotate(self.image, rot-90)
        self.rect = self.image.get_rect()
        self.pos = Vector2(pos)
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
    
    def update(self):
        if pg.time.get_ticks() - self.spawn_time > BLOOD_LIFETIME:
            self.kill()