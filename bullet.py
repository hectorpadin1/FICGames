import pygame as pg
from settings import *

'''
TODO: Implementar grupos correctamente en main, definir bien update de eventos, etc...
'''

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel + self.game.dt 
        self.rect.center = self.pos
        # Implementar correctamente muros
        #if pg.sprite.spritecollideany(self, self.game.walls):
        #    self.kill()
        if (pg.time.get_ticks() - self.spawn_time) > BULLET_LIFETIME:
            self.kill()