import pygame as pg
from settings import *

class Director():

    def __init__(self):
        # Inicializamos la pantalla
        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # Inicializamos Atributos
        self.pila = []
        self.salir_escena = False
        self.reloj = pg.time.Clock()


    def loop(self, escena):
        self.salir_escena = False
        pg.event.clear()   # Eliminamos eventos producidos -> Esto Pa k es ?????????? que podría venir que nos perjudique?
        
        while not self.salir_escena:
            dt = self.reloj.tick(60)
            # Delegamos lógicas en escena
            escena.events(pg.event.get()) #eventos gestionados por escena
            escena.update(dt)
            escena.draw(self.display)
            # Actualizamos Pantalla
            pg.display.flip()

    def run(self):
        #Ejecutamos Escenas De la Pila
        while (len(self.pila)>0):
            escena = self.pila[len(self.pila)-1]
            self.loop(escena)


    def exitEscena(self):
        self.salir_escena = True
        # Popeamos Escena
        if (len(self.pila)>0):
            self.pila.pop()
            escena = self.pila[len(self.pila)-1]
            escena.play_music()
    
    def firstEscena(self):
        self.salir_escena = True
        if (len(self.pila)>0):
            escena = self.pila[0]
            self.pila = []
            self.pila.append(escena)
            escena.play_music()

    def exitProgram(self):
        # Vaciamos pila
        self.pila = [] 
        self.salir_escena = True

    """
    def changeEscena(self, escena):
        self.salirEscena()
        # Ponemos la escena pasada en la cima de la pila
        self.pila.append(escena)
    """

    def pushEscena(self, escena):
        self.salir_escena = True
        self.pila.append(escena)

