import pygame as pg
import sys
from settings import *
from resourcemanager import ResourceManager as GR
from escenas.escena import Escena

class Menu(Escena):

    def __init__(self,director, btns, back, logo=None):
        Escena.__init__(self, director)
        self.click = False
        self.btn_group = pg.sprite.Group(*btns)
        self.back = back
        self.logo = logo

    def events(self, events):
        self.click = False
        for event in events:
            if event.type == pg.QUIT:
                self.director.exitProgram()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.click = True

    #Dibuja Caja Centrada y Devuelve su tamaño 
    def draw_box(self, display):
        bg = GR.load_image(GR.BOX_BG) 
        rect = bg.get_rect()
        rect.center = (WIDTH/2,HEIGHT/2)
        display.blit(bg, rect) 
        return rect.size
    
    #Dibuja Logo Centrado con la posibilidad de añadirle un desplazamiento
    def draw_logo(self, display, dx=0, dy=0):
        logo = GR.load_image(self.logo)
        rect = logo.get_rect()
        rect.center = (WIDTH/2+dx, HEIGHT/2+dy)
        display.blit(logo, rect) 

    def draw_back(self, display, dx=0, dy=0):
        logo = GR.load_image(GR.START_IMG)
        rect = logo.get_rect()
        rect.center = (WIDTH/2+dx, HEIGHT/2+dy)
        display.blit(logo, rect) 

    def update(self, _dt):
        mouse_pos = pg.mouse.get_pos()
        self.btn_group.update(mouse_pos,self.click)

    def draw(self,display):
        if self.back:
            self.draw_back(display, dx = 30, dy=50)

        _,box_y = self.draw_box(display)

        if self.logo is not None:
            self.draw_logo(display,dy=-((box_y/4)))

        for btn in self.btn_group:
            btn.draw(display)