import pygame as pg
from settings import *
from pygame.math import Vector2
from resourcemanager import ResourceManager as GR

class Hit(pg.sprite.Sprite):

    def __init__(self, hit_group, pos, sx, sy, rot) -> None:
        pg.sprite.Sprite.__init__(self, hit_group)
        pos = pos + Vector2(15,0).rotate(-rot)
        self.image = GR.load_image(GR.HIT_IMAGE)
        self.image = pg.transform.scale(self.image, (sx * SPRITE_BOX, sy * SPRITE_BOX))
        self.image = pg.transform.rotate(self.image, rot-90)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.pos = Vector2(pos)
        self.rect.center = Vector2(pos)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > HIT_LIFETIME:
            self.kill()