import pygame as pg
import random
from pygame.math import Vector2
from settings import *
from sprites.player import Player
from sprites.wall import Wall, Obstacle
from sprites.mob import MobBasico
from sprites.blood import Blood
from sprites.explosion import Explosion
from sprites.hit import Hit
from tiledmap import TiledMap
from camera import Camera
from soundcontroller import SoundController as SC
from escenas.escena import Escena
from escenas.gameover import GameOver
from escenas.pause import Pause


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
        self.init_game()

    def init_game(self):
        random.seed()
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
        self.bullets_player = pg.sprite.Group()
        self.bullets_mobs = pg.sprite.Group()
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
                self.player = Player(tile_object.x, tile_object.y, self.bullets_player, [self.walls, self.obstacle])
            if tile_object.name == 'Wall':
                Wall(self.walls, tile_object.x, tile_object.y, 
                        tile_object.width, tile_object.height)
            if tile_object.name == 'Object':
                Obstacle(self.obstacle, tile_object.x, tile_object.y, 
                        tile_object.width, tile_object.height)
            if tile_object.name == 'mob':
                if (random.randint(0, 1))==1:
                    x = random.randint(-50,-20) if random.randint(0,1)==1 else random.randint(20,50)
                    y = random.randint(-50,-20) if random.randint(0,1)==1 else random.randint(20,50)
                    MobBasico(self.mobs, tile_object.x +x, tile_object.y + y, self.bullets_mobs, [self.walls, self.obstacle])
                MobBasico(self.mobs, tile_object.x, tile_object.y, self.bullets_mobs, [self.walls, self.obstacle])
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False


    def __bullet_hits(self):
        # bullets hit player
        hits = pg.sprite.spritecollide(self.player, self.bullets_mobs, True, pg.sprite.collide_mask)
        for hit in hits:
            if (self.player.health - MOB_BULLET_DAMAGE) > 0:
                self.player.health -= MOB_BULLET_DAMAGE
                Hit(self.blood, self.player.pos, 0.5, 0.5, -self.player.rot-30)
                self.player.vel = Vector2(0, 0)
            else:
                self.player.health = 0
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets_player, False, True, pg.sprite.collide_mask)
        for hit in hits:
            if (hit.health - BULLET_DAMAGE) > 0:
                hit.health -= BULLET_DAMAGE
                Hit(self.blood, hit.pos, 0.5, 0.5, -hit.rot-30)
                hit.vel = Vector2(0, 0)
                hit.follow = True
            else:
                Blood(self.blood, hit.pos, 0.5, 0.5, -hit.rot-110)
                hit.kill()
        # bullet hit walls
        hits = pg.sprite.groupcollide(self.bullets_mobs, self.walls, True, False)
        for hit in hits:
            Explosion(self.explosions, hit.pos, 0.1, 0.1)
        hits = pg.sprite.groupcollide(self.bullets_player, self.walls, True, False)
        for hit in hits:
            Explosion(self.explosions, hit.pos, 0.1, 0.1)


    def update(self, dt):
        # Actualizamos grupos de sprites
        self.player.update(self.camera.camera.topleft, dt)
        self.bullets_player.update(dt)
        self.bullets_mobs.update(dt)
        self.mobs.update(self.player.pos, dt)
        self.explosions.update()
        self.blood.update()
        self.hits.update()
        # Colisiones
        self.__bullet_hits()
        # Miramos si seguimos vivos
        if self.player.health <= 0:
            Blood(self.blood, self.player.pos, 0.5, 0.5, -self.player.rot-110)
            self.gameover()

        # Posición de la cámara
        self.camera.update(self.player)


    def gameover(self):
        self.init_game() #cambiar ese __init__ por un initializegame y que init lo k haga sea llamar a lo mismo
        gameover = GameOver(self.director)
        self.director.pushEscena(gameover)


    def draw(self, display):
        
        display.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        
        # Cambiar este codigo espaguetti :)

        for sprite in self.blood:
            display.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.explosions:
            display.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.bullets_mobs:
            display.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.bullets_player:
            display.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.hits:
            display.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.mobs:
            display.blit(sprite.image, self.camera.apply(sprite))
        display.blit(self.player.image, self.camera.apply(self.player))

        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(display, (0, 255, 255), self.camera.apply_rect(wall.rect), 1)
            for obstacle in self.obstacle:
                pg.draw.rect(display, (0, 255, 255), self.camera.apply_rect(obstacle.rect), 1)
        self.player.draw_health(display, 10, 10, self.player.health / PLAYER_HEALTH)


    def events(self, events):
        for event in events:
            #Salir Ventana
            if event.type == pg.QUIT:
                self.director.exitProgram()
            #Pulsaciones Teclas
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_p: #Menu Pausa
                    pause = Pause(self.director)
                    self.director.pushEscena(pause)
                #PROVISIONAL    
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug


    def play_music(self):
        SC.play_main()

