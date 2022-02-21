import pygame as pg
from settings import *

#Revisar tema de los grupos porque me da la sensacion de que acopla mucho el código

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        #Establecemos otros sprites con los que pueda iteracionar
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        #Tamaño 
        self.image = pg.Surface((SPRITE_BOX, SPRITE_BOX))
        #Estética
        self.image.fill((255,255,220))  #Image Provisional
        #Posicion
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * SPRITE_BOX
        self.rect.y = y * SPRITE_BOX
        #print("Muro creado en " , str(self.x), str(self.y))

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        #Establecemos otros sprites con los que pueda iteracionar
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #Posicion
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
