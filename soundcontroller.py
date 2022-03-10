import pygame as pg
from settings import *
from resourcemanager import ResourceManager as GR

class SoundController:
    
    @classmethod
    def init(self):
        pg.mixer.pre_init(44100,-16,2, 3072)
        pg.mixer.init()

    @classmethod
    def play_menu(self):
        pg.mixer.music.load(START_MUSIC)
        pg.mixer.music.set_volume(0.4)
        pg.mixer.music.play(-1)
        pass

    @classmethod
    def play_main(self):
        pg.mixer.music.load(MAIN_MUSIC)
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(-1)
        pass
    
    @classmethod
    def play_gameover(self):
        pg.mixer.music.load(GAMEOVER_MUSIC)
        pg.mixer.music.play(-1)
        pass

    @classmethod
    def play_metralleta(self):
        pg.mixer.Sound.play(GR.load_sound(GR.METRALLETA))
    
    @classmethod
    def play_pistola(self):
        pg.mixer.Sound.play(GR.load_sound(GR.PISTOLA))
        
    @classmethod
    def play_ametralladora(self):
        pg.mixer.Sound.play(GR.load_sound(GR.AMETRALLADORA))
    
    @classmethod
    def play_selection(self):
        pg.mixer.Sound.play(GR.load_sound(GR.SELECTION))
    
    @classmethod
    def pause(self):
        pg.mixer.music.pause()
    
    @classmethod
    def unpause(self):
        pg.mixer.music.unpause()