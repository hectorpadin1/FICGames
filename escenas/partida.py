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
from escenas.gui.hud import Hud

        

class Partida(Escena):
    
    def __init__(self,director,lvl):
        Escena.__init__(self, director)
        self.lvl = lvl
        self.init_game()

    def init_game(self):
        random.seed()
        #Mapa
        self.map = TiledMap(self.lvl)
        #Render del mapa -> REVISAR ESTO PEDRO
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        #Hud
        self.hud = Hud()

        #self.all_sprites = pg.sprite.Group() #ESTO ES ALJO JODIAMENTE INUTIL -> BORRAR
        self.walls = pg.sprite.Group()
        self.obstacle = pg.sprite.Group()
        self.bullets_player = pg.sprite.Group()
        self.bullets_mobs = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.blood = pg.sprite.Group()
        self.hits = pg.sprite.Group()
        self.mob_count = 0

        ########################################
        #   Inicializamos cargando tiledmap    #
        ########################################
        
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(tile_object.x, tile_object.y, self.bullets_player, [self.walls, self.obstacle],[self.hud])
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
                    self.mob_count += 1
                MobBasico(self.mobs, tile_object.x, tile_object.y, self.bullets_mobs, [self.walls, self.obstacle])
                self.mob_count += 1
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False


    def __bullet_hits(self):
        # bullets hit player
        hits = pg.sprite.spritecollide(self.player, self.bullets_mobs, True, pg.sprite.collide_mask)
        for hit in hits:
            self.player.update_health(self.player.health - MOB_BULLET_DAMAGE)
            Hit(self.blood, self.player.pos, 0.5, 0.5, -self.player.rot-30)
            self.player.vel = Vector2(0, 0)
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
                self.mob_count -= 1
                hit.kill()
                if self.mob_count == 0: 
                    pause = Pause(self.director, self.lvl)
                    self.director.pushEscena(pause)
        # bullet hit walls
        hits = pg.sprite.groupcollide(self.bullets_mobs, self.walls, True, False)
        for hit in hits:
            Explosion(self.explosions, hit.pos, 0.1, 0.1)
        hits = pg.sprite.groupcollide(self.bullets_player, self.walls, True, False)
        for hit in hits:
            Explosion(self.explosions, hit.pos, 0.1, 0.1)


    def update(self, dt):
        # Miramos si seguimos vivos
        if self.player.health <= 0:
            Blood(self.blood, self.player.pos, 0.5, 0.5, -self.player.rot-110)
            self.gameover()
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

        # Posición de la cámara
        self.camera.update(self.player)


    def gameover(self):
        gameover = GameOver(self.director, self.lvl)
        self.director.changeEscena(gameover)


    def draw(self, display):
        
        display.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        
        # Cambiar este codigo espaguetti :)

        # CaESE CAMERA APPLY QUE HACE?

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

        self.hud.draw(display)


    def events(self, events):
        for event in events:
            #Salir Ventana
            if event.type == pg.QUIT:
                self.director.exitProgram()
            #Pulsaciones Teclas
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_p: #Menu Pausa
                    pause = Pause(self.director, self.lvl)
                    self.director.pushEscena(pause)


    def play_music(self):
        SC.play_main()

