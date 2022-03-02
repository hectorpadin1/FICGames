import pygame as pg

class Control:

    #abstracta control? -> yo creo k no hace falta

    #algo de este rollo
    def arriba(self,events):
        return pg.K_a in events

    def abajo(self):
        pass

    def derecha(self):
        pass   

    def izquierda(self):
        pass    

    def disparo(self):
        pass    