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
from escenas.escena import Escena


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




# self.dt = self.clock.tick(FPS) / 1000 # -> esto lo implemeta director de escena, hay que cambiarlo

    
#########################################################################################################################
#                                                                                                                       #
#  ESTO ESTÄ JODIDAMENTE MAL, INTEGRAR TILEDMAP EN ESTA MISMA CLASE                                                     #
#                                                                                                                       #
#########################################################################################################################
        

class Partida(Escena):
    
    def __init__(self,director):
        Escena.__init__(self, director)
        #Musica
        SC.play_main()
        #Mapa
        self.map = TiledMap(1)
        #Render del mapa -> REVISAR ESTO PEDRO
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.all_sprites = pg.sprite.Group() #ESTO ES ALJO JODIAMENTE INUTIL -> BORRAR
        self.walls = pg.sprite.Group()
        self.obstacle = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
    
        #########################################################################################################################
        #                                                                                                                       #
        #  ESTO VA A TOCAR PONERLO EN EL MAPA CREO YO -> que te debuelva grupos y listo -> y luego con un update/draw ya llega  #
        #                                                                                                                       #
        #########################################################################################################################
        
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

    '''
    CAMBIAR DE SITIO, a bullet por ejemplo¿?
    o que sea el jugador elq lo compruebe ¿?
    
    REVISAR ESTA FUNCIÓN
    
    '''
    def __bullet_hits(self):
        collide_hit_rect = lambda a, b : a.hit_rect.colliderect(b.rect)

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

    def update(self, dt):
        self.walls.update() #NO NECESARIO
        self.obstacle.update() #NO NECESARIO
        self.player.update(dt)
        self.bullets.update(dt)
        self.mobs.update(dt)

        self.__bullet_hits()
        self.camera.update(self.player)


    def draw(self, display):
        
        display.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #Sprites
        for sprite in self.all_sprites:
            display.blit(sprite.image, self.camera.apply(sprite)) #revisar
            if isinstance(sprite, Mob):
                sprite.draw_health()
            if self.draw_debug:
                pg.draw.rect(display, (0, 255, 255), self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(display, (0, 255, 255), self.camera.apply_rect(wall.rect), 1)
        self.player.draw_health(display, 10, 10, self.player.health / PLAYER_HEALTH)


    def events(self, events):
        for event in events:
            #Salir Ventana
            if event.type == pg.QUIT:
                self.director.exitProgram()
            #Pulsaciones Teclas
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: #Menu Pausa
                    print("Menú Pausa")
                    self.director.exitEscena()

                #PROVISIONAL    
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

