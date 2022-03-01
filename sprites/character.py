import pygame as pg
from pygame.math import Vector2
from math import cos, pi
from settings import *
from sprites.bullet import *
from sprites.common import collide_with_walls
from soundcontroller import SoundController as SC


class character(pg.sprite.Sprite):
    def __init__(self, image, x, y):
       pass
       
       #el init tiene que ser lo suficientemente genérico como para poder cargar posiciones ángulos y poco mas
    
    # la lógica de common.py debería estar aquó

    def update(self):
        pass
        
        #únicamente gestiona colisines -> resto de comportamientos dependerán de las subclases (movimientos/rotaciones)

        