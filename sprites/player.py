import pygame as pg
from pygame.math import Vector2
from math import cos, pi, atan2
from settings import *
from map import collide_hit_rect

'''
    meter grupos en entidades
    entity = Entity((320, 240))
    all_sprites = pg.sprite.Group(entity)
'''

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
        self.vel = Vector2(0, 0)
        self.pos = Vector2(x, y) * SPRITE_BOX
        self.rot = 0
        pg.mouse.set_pos((x+10) * SPRITE_BOX, y * SPRITE_BOX)
        self.mouse = pg.mouse.get_pos()

    # Dynamics of player movements
    def __get_keys(self):
        self.rot_speed = 0
        self.vel = Vector2(0, 0)
        keys = pg.key.get_pressed()
        # On-Axis movements
        if keys[pg.K_a]:
            self.vel = -Vector2(PLAYER_SPEED, 0).rotate(90-self.rot)
        if keys[pg.K_d]:
            self.vel = Vector2(PLAYER_SPEED, 0).rotate(90-self.rot)
        if keys[pg.K_w]:
            self.vel = Vector2(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_s]:
            self.vel = Vector2(-PLAYER_SPEED, 0).rotate(-self.rot)
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
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2.0
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2.0
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2.0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2.0
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y
    
    def __rotate(self):
        self.mouse = pg.mouse.get_pos()
        self.rot = -atan2(self.mouse[1] - self.pos.y, self.mouse[0] - self.pos.x) * 180 / pi

        #print(self.rot)
        '''
        coger coordenadas relativas del personaje en la pantalla
        self.pos, WIDTH, HEIGHT self.mouse
        módulo
        '''
        
    def update(self):
        # Checks where it has to move
        #if self.mouse != pg.mouse.get_pos():
        self.__rotate()
        self.__get_keys()
        #print(self.mouse, self.pos)
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # Moves in time, not in pixels, independent of our frame rate
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.__collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.__collide_with_walls('y')
        self.rect.center = self.hit_rect.center
        