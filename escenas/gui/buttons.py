import pygame as pg
import sys
from settings import *
from resourcemanager import ResourceManager as GR
from escenas.gui.button import Button

class ClasicButton(Button):
    def __init__(self, text, callback, dx=0, dy=0):
        Button.__init__(self,GR.BTN_BG, text, callback, dx=dx, dy=dy)

class LevelButton(Button):
    def __init__(self, lvl, callback, locked=False, dx=0, dy=0):
        level=str(lvl)
        if locked:
            level = "x"
            callback = lambda a : a

        Button.__init__(self,GR.LVL_BTN, level, callback, dx=dx, dy=dy)
        self.lvl=lvl
        
    def update(self, mouse_pos, click):
        self.hover = self.rect.collidepoint(mouse_pos)
        if self.hover and click:
            self.callback(self.lvl)
        
