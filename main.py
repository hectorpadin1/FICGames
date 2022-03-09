import pygame as pg
from director import Director
from escenas.start_screen import StartScreen
from soundcontroller import SoundController as SC

#Inicializamos PyGame
pg.init()
pg.mouse.set_cursor(pg.cursors.broken_x)
#Sonido
SC.init()
#SC.play_menu() # -> ponerlo donde se carga el menú?
#Inicializamos el direcor y cargamos el menú principal
director = Director()
menu_principal = StartScreen(director)
director.pushEscena(menu_principal)
director.run()
#Salimos
pg.quit()