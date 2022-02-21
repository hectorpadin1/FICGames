import pygame as pg
import sys
from settings import *

class Button:
    #Inicializamos el botón mostrándolo en pantalla
    def __init__(self, display, text, mouse_pos, callback, dx=0, dy=0):
        self.display = display #Esto No se yo si estará bien aquí -> revisar patrones
        self.callback = callback

        #Bg Btn
        bg = pg.image.load(BTN_BG)
        self.rect = bg.get_rect()
        self.rect.center = (WIDTH/2+dx,HEIGHT/2+dy)
        self.display.blit(bg, self.rect) 

        #Hovered
        self.hover = self.rect.collidepoint(mouse_pos)

        #Text
        font = pg.font.Font(MAIN_FONT,GUI_FONT_SIZE)
        color = (255,255,255)
        if self.hover:
            color = (154,122,37)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH/2+dx,HEIGHT/2+dy)
        self.display.blit(text_surface,text_rect)

    def get_size(self):
        return self.rect.size

    def exec_callback(self):
        if self.hover:
            self.callback()
        return self.hover