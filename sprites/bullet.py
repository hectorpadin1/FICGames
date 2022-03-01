import pygame as pg
from settings import *
from pygame.math import Vector2
from random import uniform
from sprites.explosion import *
from gestorrecursos import GestorRecursos as GR
from soundcontroller import SoundController as SC


class Bullet(pg.sprite.Sprite):
    
    def __init__(self, game, pos, rot):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        dir = Vector2(1, 0).rotate(-rot)
        pos = pos + BARREL_OFFSET.rotate(-rot)
        self.image = GR.load_image(GR.BULLET_IMG)
        self.image = pg.transform.rotate(self.image, rot-90)
        self.rect = self.image.get_rect()
        self.pos = Vector2(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        SC.play_metralleta()

    def kill(self,):
        Explosion(self.game.all_sprites, self.pos, 0.1, 0.1)
        super().kill()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
    