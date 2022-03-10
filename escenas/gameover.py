import pygame as pg
import sys
from settings import *
from escenas.gui.buttons import ClasicButton
from resourcemanager import ResourceManager as GR
from soundcontroller import SoundController as SC
from escenas.menu import Menu

class GameOver(Menu):

    def __init__(self, director):

        retry_btn = ClasicButton("Reintentar", self.go_retry, dy = 35)
        margin = retry_btn.get_size()[1]/2
        exit_btn = ClasicButton("Menu Principal", self.go_exit, dy=margin*4.5)
        
        Menu.__init__(self, director, [retry_btn, exit_btn], False, logo=GR.GAMEOVER_IMG)


    def go_retry(self):
        SC.play_selection()
        self.director.exitEscena()
    
    def go_exit(self):
        SC.play_selection()
        self.director.exitEscena()
        self.director.exitEscena()
    
    def play_music(self):
        SC.play_gameover()