import pygame as pg
import sys
from settings import *
from player import *

class Game:
    def __init__(self):
        pg.init()
        self.running = True
        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        #self.clock = pg.time.Clock() #meter FPS
        pg.key.set_repeat(500, 100) #habilita el mantener pulsado -> revisar tasas de refresco

    def load_data(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self, 10, 10)

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update() #revisar que actualiza

    def draw_grid(self):
        grid_color =  (125,125,12)
        #Horizontal
        for x in range(0, WIDTH, SPRITE_BOX):
            pg.draw.line(self.display, grid_color, (x, 0), (x, HEIGHT))
        #Vertical
        for y in range(0, HEIGHT, SPRITE_BOX):
            pg.draw.line(self.display, grid_color, (0, y), (WIDTH, y))

    def draw(self):
        self.display.fill((0,0,0))
        self.draw_grid()
        self.all_sprites.draw(self.display)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            #Salir Ventana
            if event.type == pg.QUIT:
                self.running=False
            #Pulsaciones Teclas
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running=False
                if event.key == pg.K_a:
                    print("left")
                    self.player.move(dx=-1)
                if event.key == pg.K_d:
                    print("right")
                    self.player.move(dx=1)
                if event.key == pg.K_w:
                    print("up")
                    self.player.move(dy=-1)
                if event.key == pg.K_s:
                    print("down")
                    self.player.move(dy=1)

    def show_start_screen(self):
        pass

    def show_end_screen(self):
        pass

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
        self.quit()

#Ciclo del juego
g = Game()
g.show_start_screen()
while True:
    g.load_data()
    g.run()
    #g.show_end_screen()