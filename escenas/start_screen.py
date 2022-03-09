import pygame as pg
import sys
from settings import *
from resourcemanager import ResourceManager as GR
from soundcontroller import SoundController as SC
from escenas.gui.buttons import ClasicButton
from escenas.menu import Menu
from escenas.partida import Partida
from escenas.level_selector import LevelSelector

class StartScreen(Menu):

    def __init__(self,director):
        SC.play_menu() #mover esto de aquí
       
        #Butones 
        play_btn  = ClasicButton("Jugar",self.go_play)
        margin    = play_btn.get_size()[1]/2 #apañar esto
        stngs_btn = ClasicButton("Ajustes",self.go_settings,dy=margin*3)
        exit_btn  = ClasicButton("Salir",self.go_exit,dy=margin*6)

        Menu.__init__(self, director, [play_btn, stngs_btn, exit_btn], True, logo=GR.LOGO_IMG)
    
    def go_play(self):
        SC.play_selection()
        lvl_selector = LevelSelector(self.director)
        self.director.pushEscena(lvl_selector)
        
    def go_settings(self):
        SC.play_selection()
        print("settings")

    def go_exit(self):
        pg.quit()
        sys.exit()      
    
    def play_music(self):
        SC.play_menu()
