import pygame as pg
import sys
from settings import *
from escenas.gui.buttons import ClasicButton, LevelButton
from managers.resourcemanager import ResourceManager as GR
from managers.soundcontroller import SoundController as SC
from escenas.menu import Menu
from escenas.partida import Partida
from managers.user_config import UserConfig as UC

class LevelSelector(Menu):

    def __init__(self,director):
        #Read Config
        last_level = 0
        self.last_check = pg.time.get_ticks()
        try:
            last_level = UC.get("last_level")
        except:
            pass
        lvl_btns = []
        margin = -52*3
        for i in range(0,5):
            lvl_btns.append(LevelButton(i,self.go_play,dx=margin, dy=26, locked=(i>last_level)))
            margin=margin+52*1.5

        lvl_btns.append(ClasicButton("Volver",self.go_back, dy=80+26))

        Menu.__init__(self, director, lvl_btns, True, logo=GR.LOGO_IMG)
    
    
    def update(self, _dt):
        Menu.update(self,_dt)
        now =  pg.time.get_ticks()
        if now - self.last_check > 10000: #Cada 10s
            try:
                last_level = UC.get("last_level")
            except:
                pass
            self.last_check = pg.time.get_ticks()

    #Callbacks

    def go_play(self,lvl):
        SC.play_selection()
        partida = Partida(self.director,lvl)
        self.director.pushEscena(partida,)

    def go_back(self):
        SC.play_selection()
        self.director.exitEscena(updateMusic = False)
    
    def play_music(self):
        SC.play_menu()
