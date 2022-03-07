import pygame as pg
import sys
from settings import *
from gui.button import Button
from gui.button import LevelButton
from gestorrecursos import GestorRecursos as GR
from soundcontroller import SoundController as SC
from escenas.escena import Escena
from escenas.partida import Partida

class LevelSelector(Escena):

    def __init__(self,director):
        Escena.__init__(self, director)
        SC.play_menu()
        self.click = False
        #Butones 
        self.lvl_btns = []
        for i in range(0,1):
            self.lvl_btns + [LevelButton(str(i),lamb)]
        self.play_btn  = Button("Volver",self.go_play)

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
        logo = GR.load_image(GR.LOGO_IMG)
        rect = logo.get_rect()
        rect.center = (WIDTH/2+dx, HEIGHT/2+dy)
        display.blit(logo, rect) 


    def update(self, _dt):
        mouse_pos = pg.mouse.get_pos()
        self.play_btn.update(mouse_pos,self.click)
        self.stngs_btn.update(mouse_pos,self.click)
        self.exit_btn.update(mouse_pos,self.click)

    def draw(self,display):
        display.fill((66,82,58)) # fondo provisional

        _,box_y = self.draw_box(display)
        self.draw_logo(display,dy=-((box_y/4)))

        self.play_btn.draw(display)
        self.stngs_btn.draw(display)
        self.exit_btn.draw(display)
    
    def go_play(self,lvl):
        SC.play_selection()
        partida = Partida(self.director)
        self.director.pushEscena(partida)

    def go_back(self):
        SC.play_selection()
        self.director.exitEscena()


    def play_music(self):
        SC.play_menu()
