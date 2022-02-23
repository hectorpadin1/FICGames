import pygame as pg
from settings import *
from pygame.math import Vector2

class Mob(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(MOB_IMAGE).convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = Vector2(x, y) * SPRITE_BOX
        self.rect.center = self.pos
        self.rot = 0

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(Vector2(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos