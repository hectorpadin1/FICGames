import pygame as pg
from director import Director
from escenas.start_screen import StartScreen
from soundcontroller import SoundController as SC
from user_config import UserConfig as UC

#Inicializamos PyGame
pg.init()
pg.mouse.set_cursor(pg.cursors.broken_x)
#Sonido
SC.init()
UC.init()
#Inicializamos el direcor y cargamos el menú principal
director = Director()
menu_principal = StartScreen(director)
director.pushEscena(menu_principal)
director.run()
#Salimos
pg.quit()