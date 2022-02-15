import pygame as pg
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
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        if not self.__collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
    
    def __collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * SPRITE_BOX
        self.rect.y = self.y * SPRITE_BOX