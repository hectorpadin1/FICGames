import pygame as pg
import sys
from settings import *
from resourcemanager import ResourceManager as GR

class Hud():
    #Inicializamos el botón mostrándolo en pantalla
    def __init__(self):
        self.gun = None
        self.life= 90

        self.image = GR.load_image(GR.HUD)
        self.rect = self.image.get_rect() 
        self.rect.bottomleft = (0,HEIGHT)


        #Vida
        font = GR.load_font(GR.MAIN_FONT,19)
        self.life_surface = font.render(str(self.life)+"%", True, (255,255,255))
        self.life_rect = self.life_surface.get_rect()
        self.life_rect.center = (237,HEIGHT-38)

        #Ammo
        font = GR.load_font(GR.MAIN_FONT,16) #
        self.ammo_surface = font.render("10/33", True, (255,255,255))
        self.ammo_rect = self.ammo_surface.get_rect()
        self.ammo_rect.center = (90,HEIGHT-123)

    def update(self):
        pass
        
    def draw(self, display):
        display.blit(self.image, self.rect) 
        display.blit(self.life_surface, self.life_rect) 
        display.blit(self.ammo_surface, self.ammo_rect) 
    
