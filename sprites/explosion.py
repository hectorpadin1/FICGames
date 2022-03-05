import pygame as pg
from settings import *
from pygame.math import Vector2
from gestorrecursos import GestorRecursos as GR

#
#   NO DESAPARECEN PORQUE NO SE EJECUTA EL UPDATE -> hector gestiona los grupos bien y mételo
#


class Explosion(pg.sprite.Sprite):

    def __init__(self, explosion_group, pos, sx, sy) -> None:
        pg.sprite.Sprite.__init__(self, explosion_group)
        self.pos = pos
        self.image = GR.load_image(GR.EXPLOSION_IMAGE)
        self.image = pg.transform.scale(self.image, (sx * SPRITE_BOX, sy * SPRITE_BOX))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.pos = Vector2(pos)
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
    
    def update(self):
        if pg.time.get_ticks() - self.spawn_time > EXPLOSION_LIFETIME:
            self.kill()