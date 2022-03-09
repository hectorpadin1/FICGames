import pygame as pg
import sys
from settings import *
from escenas.gui.buttons import ClasicButton, LevelButton
from resourcemanager import ResourceManager as GR
from soundcontroller import SoundController as SC
from escenas.menu import Menu
from escenas.partida import Partida

class LevelSelector(Menu):

    def __init__(self,director):
        lvl_btns = []
        margin = -52*3
        for i in range(0,5):
            lvl_btns.append(LevelButton(i,self.go_play,dx=margin, dy=26))
            margin=margin+52*1.5

        lvl_btns.append(ClasicButton("Volver",self.go_back, dy=80+26))

        Menu.__init__(self, director, lvl_btns, True, logo=GR.LOGO_IMG)


    #Callbacks

    def go_play(self,lvl):
        SC.play_selection()
        partida = Partida(self.director,lvl)
        self.director.pushEscena(partida)

    def go_back(self):
        SC.play_selection()
        self.director.exitEscena()

