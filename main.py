import pygame as pg
import sys
from os import path
from settings import *
from sprites.player import *
from sprites.wall import *
from sprites.bullet import *
from map import *

# Revisar:
#   - dudas don draw()
#       -display.update vs display flip ??
#       -display blit -> for sprites?

# Dudas: 
#   - acoplamiento de sprites al juego
#   - Grupos -> sprite añade a los grupos que se le pasan, pero es necesario pasarle el juego ¿?
#   - Acoplamiento del juego en los sprites
#
#
#
#
#
#
#


class Game:
    #Inicializamos Juego
    def __init__(self):
        pg.init()
        self.running = True
        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock() #revisar
        self.load_data()

    #Cargamos Recursos
    def load_data(self):
        game_folder = path.dirname(__file__)
        #Mapa
        self.map = Map(path.join(game_folder, 'map.txt'))
        #Assets
        self.player_img = pg.image.load(path.join(game_folder, PLAYER_IMG)).convert_alpha()
        #falta tileset, menus...

    #Creamos partida: inicializamos sprites 
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        #self.bullets = pg.sprite.Group()
        # Loading initial map for testing
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    #Salir
    def quit(self):
        pg.quit()
        sys.exit()

    #Actualiza Sprites (muros no) y Camara
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)


    ###TEMPORAL###
    def draw_grid(self):
        grid_color = (125,125,12)
        #Horizontal
        for x in range(0, WIDTH, SPRITE_BOX):
            pg.draw.line(self.display, grid_color, (x, 0), (x, HEIGHT))
        #Vertical
        for y in range(0, HEIGHT, SPRITE_BOX):
            pg.draw.line(self.display, grid_color, (0, y), (WIDTH, y))

    #Pinta
    def draw(self):
        self.display.fill((0,0,0)) #Fondo
        self.draw_grid()#tmp
        #Sprites
        for sprite in self.all_sprites:
            self.display.blit(sprite.image, self.camera.apply(sprite)) #revisar
        #Actualizamos Pantalla
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            #Salir Ventana
            if event.type == pg.QUIT:
                self.running=False
            #Pulsaciones Teclas
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_end_screen(self):
        pass

    #Bucle de Partida
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 #diferencia de tiempo
            self.events()
            self.update()
            self.draw()

#Ciclo Juego
if (__name__ == "__main__"):    
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_go_screen()