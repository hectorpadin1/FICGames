import pygame as pg
from settings import *
from resourcemanager import ResourceManager as GR

class Ammo(pg.sprite.Sprite):

    def __init__(self, item_group, x, y):
        pg.sprite.Sprite.__init__(self, item_group)
        self.image = GR.load_image(GR.AMMO_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

