import pygame as pg
from math import cos, sin, pi
from settings import *


class Player(pg.sprite.Sprite):
    #NO ME MOLA NADA COMO SE ESTÁ ACOPLANDO TODO EL JUEGO, MIRAR DE SIMPLEMENTE DAR DE ALTA EL SPRITE
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((SPRITE_BOX, SPRITE_BOX))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * SPRITE_BOX
        self.y = y * SPRITE_BOX

    # Dynamics of player movements
    def __get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        # On-Axis movements
        if keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        # Oposite movements
        if keys[pg.K_a] and keys[pg.K_d]:
            self.vx = 0
        if keys[pg.K_w] and keys[pg.K_s]:
            self.vy = 0
        # Diagonal movements        
        if self.vx!=0 and self.vy !=0:
            self.vx *= cos(pi/4)
            self.vy *= sin(pi/4)
    
    def __collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        # Checks where it has to move
        self.__get_keys()
        # Moves in time, not in pixels, independent of our frame rate
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.__collide_with_walls('x')
        self.rect.y = self.y
        self.__collide_with_walls('y')
        