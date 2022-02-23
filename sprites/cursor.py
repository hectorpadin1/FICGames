import pygame as pg
from settings import *

class Cursor(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.cursor_img
        self.rect = self.image.get_rect()
        self.rect.center = pg.mouse.get_pos()