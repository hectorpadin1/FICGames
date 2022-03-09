import pygame as pg
import sys
from settings import *
from escenas.gui.button import Button
from escenas.gui.level_button import LevelButton
from resourcemanager import ResourceManager as GR
from soundcontroller import SoundController as SC
from escenas.escena import Escena
from escenas.partida import Partida

class LevelSelector(Escena):

    def __init__(self,director):
        Escena.__init__(self, director)
        self.click = False
        #Butones 
        self.lvl_btns = []
        margin = -52*3
        for i in range(0,5):
            self.lvl_btns.append(LevelButton(str(i),self.go_play,dx=margin, dy=26))
            margin=margin+52*1.5

        self.back_btn  = Button("Volver",self.go_back, dy=80+26)

    def events(self, events):
        self.click = False
        for event in events:
            if event.type == pg.QUIT:
                self.director.exitProgram()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.click = True

    def update(self, _dt):
        mouse_pos = pg.mouse.get_pos()
        for btn in self.lvl_btns:
            btn.update(mouse_pos,self.click)
        self.back_btn.update(mouse_pos,self.click)

    #Dibuja Caja Centrada y Devuelve su tamaño 
    def draw_box(self, display):
        bg = GR.load_image(GR.BOX_BG) 
        rect = bg.get_rect()
        rect.center = (WIDTH/2,HEIGHT/2)
        display.blit(bg, rect) 
        return rect.size

    def draw_logo(self, display, dx=0, dy=0):
        logo = GR.load_image(GR.SELECT_LOGO)
        rect = logo.get_rect()
        rect.center = (WIDTH/2+dx, HEIGHT/2+dy)
        display.blit(logo, rect) 
            
    def draw_back(self, display, dx=0, dy=0):
        logo = GR.load_image(GR.START_IMG)
        rect = logo.get_rect()
        rect.center = (WIDTH/2+dx, HEIGHT/2+dy)
        display.blit(logo, rect) 

    def draw(self,display):
        self.draw_back(display, dx = 30, dy=50)

        _,box_y = self.draw_box(display)
        
        self.draw_logo(display,dy=-((box_y/5)))


        for btn in self.lvl_btns:
            btn.draw(display)

        self.back_btn.draw(display)
    
    #Callbacks

    def go_play(self,lvl):
        SC.play_selection()
        partida = Partida(self.director,lvl)
        self.director.pushEscena(partida)

    def go_back(self):
        SC.play_selection()
        self.director.exitEscena()

