import pygame as pg
from math import cos, sin, pi
from settings import *


class Player(pg.sprite.Sprite):
    #NO ME MOLA NADA COMO SE ESTÁ ACOPLANDO TODO EL JUEGO, MIRAR DE SIMPLEMENTE DAR DE ALTA EL SPRITE
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.rect = self.image.get_rect()
        self.vel = pg.math.Vector2(0, 0)
        self.pos = pg.math.Vector2(x, y) * SPRITE_BOX

    # Dynamics of player movements
    def __get_keys(self):
        self.vel = pg.math.Vector2(0, 0)
        keys = pg.key.get_pressed()
        # On-Axis movements
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        # Oposite movements
        if keys[pg.K_a] and keys[pg.K_d]:
            self.vel.x = 0
        if keys[pg.K_w] and keys[pg.K_s]:
            self.vel.y = 0
        # Diagonal movements        
        if self.vel.x!=0 and self.vel.y !=0:
            self.vel *= cos(pi/4)
    
    def __collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        # Checks where it has to move
        self.__get_keys()
        # Moves in time, not in pixels, independent of our frame rate
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.__collide_with_walls('x')
        self.rect.y = self.pos.y
        self.__collide_with_walls('y')
        