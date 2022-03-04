import pygame as pg
from settings import *
from gestorrecursos import GestorRecursos as GR

class SoundController:
    
    @classmethod
    def init(self):
        pg.mixer.pre_init(44100,-16,2, 3072)
        pg.mixer.init()

    @classmethod
    def play_menu(self):
        pg.mixer.music.load(START_MUSIC)
        pg.mixer.music.play(-1)
        pass

    @classmethod
    def play_main(self):
        #pg.mixer.music.load(MAIN_MUSIC)
        #pg.mixer.music.play(-1)
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
    def play_selection(self):
        pg.mixer.music.pause()
        pg.mixer.Sound.play(GR.load_sound(GR.SELECTION))