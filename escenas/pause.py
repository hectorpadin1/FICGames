import pygame as pg
import sys
from settings import *
from escenas.gui.button import Button
from resourcemanager import ResourceManager as GR
from soundcontroller import SoundController as SC
from escenas.escena import Escena
import escenas.partida

class Pause(Escena):

    def __init__(self, director):
        Escena.__init__(self, director)
        SC.play_gameover()
        self.click = False
        #Buttons
        self.continue_btn = Button("Continuar", self.go_continue, dy = 5)
        margin = self.continue_btn.get_size()[1]/2
        self.retry_btn = Button("Reintentar", self.go_retry, dy = margin*3.22)
        self.exit_btn = Button("Menu Principal", self.go_exit, dy=margin*6)
    
    def events(self, events):
        self.click = False
        for event in events:
            if event.type == pg.QUIT:
                SC.play_selection()
            #Pulsaciones Teclas
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_p:
                    self.go_continue()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.click = True
    
    #Dibuja Caja Centrada y Devuelve su tamaño 
    def draw_box(self, display):
        bg = GR.load_image(GR.BOX_GO) 
        rect = bg.get_rect()
        rect.center = (WIDTH/2,HEIGHT/2)
        display.blit(bg, rect) 
        return rect.size
    
    #Dibuja Logo Centrado con la posibilidad de añadirle un desplazamiento
    def draw_logo(self, display, dx=0, dy=0):
        logo = GR.load_image(GR.PAUSE_IMG)
        rect = logo.get_rect()
        rect.center = (WIDTH/2+dx, HEIGHT/2+dy)
        display.blit(logo, rect) 
    
    def update(self, _dt):
        mouse_pos = pg.mouse.get_pos()
        self.continue_btn.update(mouse_pos,self.click)
        self.retry_btn.update(mouse_pos,self.click)
        self.exit_btn.update(mouse_pos,self.click)

    def draw(self,display):
        #display.fill((66,82,58)) # fondo provisional

        _,box_y = self.draw_box(display)
        self.draw_logo(display,dy=-((box_y/4)))

        self.continue_btn.draw(display)
        self.retry_btn.draw(display)
        self.exit_btn.draw(display)
    
    def go_continue(self):
        self.director.exitEscena()
    
    def go_retry(self):
        SC.play_selection()
        partida = escenas.partida.Partida(self.director,"polla")
        self.director.exitEscena()
        self.director.exitEscena()
        self.director.pushEscena(partida)
        
    def go_exit(self):
        SC.play_selection()
        self.director.exitEscena()
        self.director.exitEscena()
    
    def play_music(self):
        pass
