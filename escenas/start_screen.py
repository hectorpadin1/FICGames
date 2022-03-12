import pygame as pg
import sys
from settings import *
from managers.resourcemanager import ResourceManager as GR
from managers.soundcontroller import SoundController as SC
from escenas.gui.buttons import ClasicButton
from escenas.menu import Menu
from escenas.level_selector import LevelSelector
from escenas.settings import Settings

class StartScreen(Menu):

    def __init__(self,director):       
        #Butones 
        play_btn  = ClasicButton("Jugar",self.go_play)
        margin    = play_btn.get_size()[1]/2 #apañar esto
        stngs_btn = ClasicButton("Ajustes",self.go_settings,dy=margin*3)
        exit_btn  = ClasicButton("Salir",self.go_exit,dy=margin*6)

        Menu.__init__(self, director, [play_btn, stngs_btn, exit_btn], True, logo=GR.LOGO_IMG)
    
    def go_play(self):
        SC.play_selection()
        lvl_selector = LevelSelector(self.director)
        self.director.pushEscena(lvl_selector, updateMusic = False)
        
    def go_settings(self):
        SC.play_selection()
        stg = Settings(self.director)
        self.director.pushEscena(stg, updateMusic = False)

    def go_exit(self):
        pg.quit()
        sys.exit()      
    
    def play_music(self):
        SC.play_menu()
