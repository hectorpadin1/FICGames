import pygame as pg
import sys
from os import path
from settings import *
from sprites.player import *
from sprites.wall import *
from sprites.bullet import *
from sprites.mob import *
from gui.start_screen import *
from tiledmap import *
from camera import *
from soundcontroller import SoundController as SC

# Revisar:
#   audio esta como el ojete, cargarse todos los pg.mixer.music -> y usar sounds.py

#diccionario nivel-fichero -> inyeccion dependencias (patrón factoría)
#gestor de recursos -> sigleton creo que era como un decoradors
#gui última llamada y fuera

# Dudas: 
#   - acoplamiento de sprites al juego
#   - Grupos -> sprite añade a los grupos que se le pasan, pero es necesario pasarle el juego ¿?
#   - Acoplamiento del juego en los sprites
#   - Para el ratón en la UI, usamos eventos o raton get pos??


#
# Idea:
#   - mapa para el fondo de la pantalla de carga -> un helicóptero y cosas -> si no lo ponemos color cesped
#   - poner subtexto debajo del título en menu de inicio
#   - cambiar captions en menus

def collide_hit_rect(one, two):
        return one.hit_rect.colliderect(two.rect)

class Game:
    
    def __init__(self):
        #Inicializamos
        pg.init()
        pg.display.set_caption(TITLE)
        pg.mouse.set_cursor(*pg.cursors.broken_x)
        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        #Sonido
        SC.init()
        SC.play_menu() # -> ponerlo donde se carga el menú?

        self.running = True
        self.start_screen = StartScreen(self.display)
        self.load_data()


    #Cargamos Recursos -> Borrarlo en un futuro
    def load_data(self):
        #Mapa
        self.map = TiledMap(1)
        #Render del mapa
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    

    #Creamos partida: inicializamos sprites -> esto está mal aqui, tendrá que ir a la fase correspondiente
    def new(self):
        #Música
        SC.play_main()

        #Grupos
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.obstacle = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()

        # Initial pos of player and collisions
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y, [self.walls, self.obstacle])
                #Mob(self, tile_object.x+10, tile_object.y)
            if tile_object.name == 'Wall':
                Wall(self, tile_object.x, tile_object.y, 
                        tile_object.width, tile_object.height)
            if tile_object.name == 'Object':
                Obstacle(self, tile_object.x, tile_object.y, 
                        tile_object.width, tile_object.height)
            if tile_object.name == 'mob':
                # dd cojones se spawnea esto xdddd
                Mob(self, tile_object.x, tile_object.y, [self.walls, self.obstacle])
        Mob(self, 700, 1560, [self.walls, self.obstacle])
        Mob(self, 700, 1560, [self.walls, self.obstacle])
        Mob(self, 700, 1560, [self.walls, self.obstacle])
        Mob(self, 700, 1560, [self.walls, self.obstacle])
        Mob(self, 700, 1560, [self.walls, self.obstacle])
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    #Salir
    def quit(self):
        pg.quit()
        sys.exit()

    '''
    CAMBIAR DE SITIO, a bullet por ejemplo¿?
    o que sea el jugador elq lo compruebe ¿?
    '''
    
    def bullet_hits(self):
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = Vector2(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += Vector2(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = Vector2(0, 0)

    #Actualiza Sprites (muros no) y Camara
    def update(self):
        self.all_sprites.update()
        self.bullet_hits()
        self.camera.update(self.player)


    def draw(self):
        
        self.display.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #Sprites
        for sprite in self.all_sprites:
            self.display.blit(sprite.image, self.camera.apply(sprite)) #revisar
            if isinstance(sprite, Mob):
                sprite.draw_health()
            if self.draw_debug:
                pg.draw.rect(self.display, (0, 255, 255), self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.display, (0, 255, 255), self.camera.apply_rect(wall.rect), 1)
        self.player.draw_health(self.display, 10, 10, self.player.health / PLAYER_HEALTH)
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
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
    #Bucle de Partida
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 #diferencia de tiempo
            self.events()
            self.update()
            self.draw()


    def show_start_screen(self):
        return self.start_screen.loop()
        # POSIBILIDAD -> reflexional una vez acabado
        # Orientado a hacer más sencillos los menus de pausa y la ui
        #Este bucle podría ser interesante combinarlo con el run, de forma que solo haya un bucle infinito que printee algo -> ej run( print_fn() ), pudiendo ser la print_fn de la start screen o del juego

    def show_gameover(self):
        pass


#Ciclo Juego
if (__name__ == "__main__"):    
    g = Game()
    level = g.show_start_screen()
    while True:
        g.new() #load level
        g.run()
        g.show_gameover()