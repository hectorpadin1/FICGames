import pygame as pg
import sys
from os import path
from math import cos, pi
from settings import *
from sprites.player import Player
from sprites.wall import Wall, Obstacle
from sprites.bullet import Bullet
from sprites.mob import Mob
from sprites.blood import Blood
from sprites.explosion import Explosion
from sprites.hit import Hit
from gui.start_screen import *
from tiledmap import TiledMap
from camera import Camera
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

        #self.all_sprites = pg.sprite.Group() #ESTO ES ALJO JODIAMENTE INUTIL -> BORRAR
        self.walls = pg.sprite.Group()
        self.obstacle = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.blood = pg.sprite.Group()
        self.hits = pg.sprite.Group()

        #########################################################################################################################
        #                                                                                                                       #
        #  ESTO VA A TOCAR PONERLO EN EL MAPA CREO YO -> que te debuelva grupos y listo -> y luego con un update/draw ya llega  #
        #                                                                                                                       #
        #########################################################################################################################

        # Initial pos of player and collisions
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(tile_object.x, tile_object.y, [self.walls, self.obstacle])
                #Mob(self, tile_object.x+10, tile_object.y)
            if tile_object.name == 'Wall':
                Wall(self.walls, tile_object.x, tile_object.y, 
                        tile_object.width, tile_object.height)
            if tile_object.name == 'Object':
                Obstacle(self.obstacle, tile_object.x, tile_object.y, 
                        tile_object.width, tile_object.height)
            if tile_object.name == 'mob':
                # dd cojones se spawnea esto xdddd
                Mob(self.mobs, tile_object.x, tile_object.y, [self.walls, self.obstacle])
        Mob(self.mobs, 700, 1560, [self.walls, self.obstacle])
        Mob(self.mobs, 700, 1560, [self.walls, self.obstacle])
        Mob(self.mobs, 700, 1560, [self.walls, self.obstacle])
        Mob(self.mobs, 700, 1560, [self.walls, self.obstacle])
        Mob(self.mobs, 700, 1560, [self.walls, self.obstacle])
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False


    def __bullet_hits(self):
        collide_hit_rect = lambda a, b : a.hit_rect.colliderect(b.rect)
        # mobs hit player -> tienen que disparar por eso pongo aqui esto
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            hit.vel = Vector2(0, 0)
            if (self.player.health - MOB_DAMAGE) > 0:
                self.player.health -= MOB_DAMAGE
            else:
                self.player.health = 0
        if hits:
            self.player.pos += Vector2(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            if (hit.health - BULLET_DAMAGE) > 0:
                hit.health -= BULLET_DAMAGE
                Hit(self.blood, hit.pos, 0.5, 0.5, -hit.rot-30)
                hit.vel = Vector2(0, 0)
            else:
                Blood(self.blood, hit.pos, 0.5, 0.5, -hit.rot-110)
                hit.kill()
        # bullet hit walls
        hits = pg.sprite.groupcollide(self.bullets, self.walls, True, False)
        for hit in hits:
            Explosion(self.explosions, hit.pos, 0.1, 0.1)


    def update(self, dt):
        # Actualizamos grupos de sprites
        self.player.update(self.camera.camera.topleft, dt)
        # Esto no mg
        if self.player.shooting:
            now = pg.time.get_ticks()
            if now - self.player.last_shot > BULLET_RATE:
                self.player.last_shot = now
                Bullet(self.bullets, self.player.pos, self.player.rot)
        self.bullets.update(dt)
        self.mobs.update(self.player.pos, dt)
        self.explosions.update()
        self.blood.update()
        self.hits.update()
        # Colisiones
        self.__bullet_hits()
        # Miramos si seguimos vivos
        if self.player.health <= 0:
            self.director.exitEscena()
        # Posición de la cámara
        self.camera.update(self.player)


    def draw(self, display):
        
        display.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        
        # Cambiar este codigo espaguetti :)

        for sprite in self.blood:
            display.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.explosions:
            display.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.bullets:
            display.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.hits:
            display.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.mobs:
            display.blit(sprite.image, self.camera.apply(sprite))
        display.blit(self.player.image, self.camera.apply(self.player))

        #for sprite in self.all_sprites:
        #    display.blit(sprite.image, self.camera.apply(sprite)) #revisar
        #    if isinstance(sprite, Mob):
        #        sprite.draw_health()
        #    if self.draw_debug:
        #        pg.draw.rect(display, (0, 255, 255), self.camera.apply_rect(sprite.hit_rect), 1)
        #if self.draw_debug:
        #    for wall in self.walls:
        #        pg.draw.rect(display, (0, 255, 255), self.camera.apply_rect(wall.rect), 1)
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
        # Player dynamics
        self.player.rot_speed = 0
        self.player.vel = Vector2(0, 0)
        keys = pg.key.get_pressed()
        # On-Axis movements
        if keys[pg.K_a]:
            self.player.vel.x = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.player.vel.x = PLAYER_SPEED
        if keys[pg.K_w]:
            self.player.vel.y = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.player.vel.y = PLAYER_SPEED
        # Oposite movements
        if keys[pg.K_a] and keys[pg.K_d]:
            self.player.vel.x = 0
        if keys[pg.K_w] and keys[pg.K_s]:
            self.player.vel.y = 0
        # Diagonal movements        
        if self.player.vel.x!=0 and self.player.vel.y !=0:
            self.player.vel *= cos(pi/4)
        # Mirar de cambiar esto
        if keys[pg.K_SPACE]:
            self.player.shooting = True
        else:
            self.player.shooting = False
    
    def play_music(self):
        SC.play_main()

