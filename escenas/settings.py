import pygame as pg
import sys
from settings import *
from resourcemanager import ResourceManager as GR
from soundcontroller import SoundController as SC
from escenas.gui.buttons import ToogleButton, LevelButton, ClasicButton
from escenas.menu import Menu

class Settings(Menu):

    def __init__(self,director):       
        #Butones 
        margin = 22
        fullscreen  = ToogleButton(director.is_fullscreen(),self.do_fullscreen,dy=-margin*5)
        self.musicy_margin = 4
        up_music = LevelButton("+",self.do_up_music,dy=self.musicy_margin, dx=margin*3)
        down_music  = LevelButton("-",self.do_down_music,dy=self.musicy_margin,dx=-margin*3)
        self.soundy_margin = margin*5
        up_sound = LevelButton("+",self.do_up_sound,dy=self.soundy_margin, dx=margin*3)
        down_sound  = LevelButton("-",self.do_down_sound,dy=self.soundy_margin,dx=-margin*3)
        controls = ClasicButton("Volver",self.go_back,dy=margin*8)
        Menu.__init__(self, director, [fullscreen, up_music, down_music, up_sound, down_sound, controls], True)

        #Texto
        self.draw_list = []
        self.font = GR.load_font(GR.MAIN_FONT,GUI_FONT_SIZE)
        self.add_text("FullScreen", -margin*7)
        self.add_text("Music", -margin*2.2)
        self.add_text("Sound Effects", margin*2.7)


    def add_text(self,text,dy,display=None):
        text = self.font.render(text, True, (255,255,255))
        text_rect = text.get_rect()
        text_rect.center = (WIDTH/2,HEIGHT/2+dy)
        if display is None:
            self.draw_list.append((text,text_rect))
        else:
            display.blit(text,text_rect)   

    def draw(self, display):
        Menu.draw(self,display)
        for (a,b) in self.draw_list:
            display.blit(a,b)   
        #Draw Values   
        self.add_text(str(SC.get_music_volume()), self.musicy_margin, display=display)
        self.add_text(str(SC.get_sound_volume()), self.soundy_margin, display=display)

    
    def do_fullscreen(self):
        SC.play_selection()
        self.director.toogle_fullscreen()

    def do_up_music(self,_):
        SC.play_selection()

    def do_down_music(self,_):
        SC.play_selection()

    def do_up_sound(self,_):
        SC.play_selection()

    def do_down_sound(self,_):
        SC.play_selection()
        
        
    def go_back(self):
        SC.play_selection()
        self.director.exitEscena()


