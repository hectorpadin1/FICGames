import pygame as pg
from settings import *

def start():
    pg.mixer.pre_init(44100,-16,2, 3072)
    
def play_menu():
    pg.mixer.music.load(START_MUSIC)
    pg.mixer.music.play(-1)

def play_main():
    pg.mixer.music.load(MAIN_MUSIC)
    pg.mixer.music.play(-1)

def play_metralleta():
    pg.mixer.Sound.play(pg.mixer.Sound(METRALLETA))

def play_selection():
    pg.mixer.music.pause()
    pg.mixer.Sound.play(pg.mixer.Sound(SELECTION))