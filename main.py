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
#       -display blit -> for sprites? -> printea en superficie, pero sobre el center o klk???


# Dudas: 
#   - acoplamiento de sprites al juego
#   - Grupos -> sprite añade a los grupos que se le pasan, pero es necesario pasarle el juego ¿?
#   - Acoplamiento del juego en los sprites
#   
#


#
# Idea:
#   - mapa para el fondo de la pantalla de carga -> un helicóptero y cosas -> si no lo ponemos color cesped
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
                #tendremos que cambiarlo para el menu de pausa
                if event.key == pg.K_ESCAPE:
                    self.quit()

    #Bucle de Partida
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 #diferencia de tiempo
            self.events()
            self.update()
            self.draw()


    #
    #   ESTO SE DEBERÏA MOVERE A UNA CLASE UI
    # 
    def draw_text(self, text, size, x, y ):
        font = pg.font.Font("ModernDOS9x16.ttf",size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def draw_button(self, text, size, x, y ):
        #Bg Btn
        bg = pg.image.load(BTN_BG)
        rect = bg.get_rect()
        rect.center = (x,y)
        self.display.blit(bg, rect) 

        #Text
        font = pg.font.Font("ModernDOS9x16.ttf",size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def draw_box(self):

        bg = pg.image.load(BOX_BG)
        rect = bg.get_rect()
        rect.center = (WIDTH/2,HEIGHT/2)
        self.display.blit(bg, rect) 

        #Version que cargaba caja como rectangulo
        #sx,sy = GUI_BOX_SIZE
        #pg.draw.rect(self.display, GUI_COLOR, ((WIDTH/2-sx/2),(HEIGHT/2-sy/2),sx,sy), 0)

    def draw_logo(self):
        logo = pg.image.load(LOGO_IMG)
        rect = logo.get_rect()
        rect.center = (WIDTH/2, HEIGHT/2-128) #harcodeado meter de alguna forma mas elegante las distancias
        self.display.blit(logo, rect) #Bua es que esta piche func no me queda claro lo que hace
    #
    #   AQUI ACABA LO QUE NO DEBERÏA ESTAR AQUÍ
    #   


    def start_screen(self):
        while True:
            #Mouse
            self.events() #sin esto no va wtf -> diferencia de pillarlo con pg.mouse o eventos
            pos = pg.mouse.get_pos()
            print(pos)
      
            #DRAWING
            self.display.fill((66,82,58)) #BG
            self.draw_box() 
            self.draw_logo()

            self.draw_button("culo",20,WIDTH/2, HEIGHT/2)

            pg.display.update() #diferencia conflip?
        return 1


    def show_end_screen(self):
        pass


#Ciclo Juego
if (__name__ == "__main__"):    
    g = Game()
    level = g.start_screen()
    while True:
        g.new() #load level
        g.run()
        g.show_go_screen()