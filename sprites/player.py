import pygame as pg
from pygame.math import Vector2
from math import cos, pi
from settings import *
from sprites.bullet import *
from sprites.common import collide_with_walls
from soundcontroller import SoundController as SC


#NO ME MOLA NADA COMO SE ESTÁ ACOPLANDO TODO EL JUEGO, MIRAR DE SIMPLEMENTE DAR DE ALTA EL SPRITE

#ESTA FATAL, ACOPLADÏSIMO

class Player(pg.sprite.Sprite):
    def __init__(self, game,x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = GR.load_image(GR.PLAYER_IMG)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = Vector2(0, 0)
        self.pos = Vector2(x, y)
        self.rot = 0
        self.last_shot = 0
        pg.mouse.set_pos((x+10) * SPRITE_BOX, y * SPRITE_BOX)
        self.mouse = pg.mouse.get_pos()
        self.health = PLAYER_HEALTH
    
    # Dynamics of player movements
    def __get_keys(self):
        self.rot_speed = 0
        self.vel = Vector2(0, 0)
        keys = pg.key.get_pressed()
        # On-Axis movements
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        # Oposite movements
        if keys[pg.K_a] and keys[pg.K_d]:
            self.vel.x = 0
        if keys[pg.K_w] and keys[pg.K_s]:   
            self.vel.y = 0
        # Diagonal movements        
        if self.vel.x!=0 and self.vel.y !=0:
            self.vel *= cos(pi/4)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                Bullet(self.game, self.pos, self.rot)
        
    def __rotate(self):
        direction = pg.mouse.get_pos() - Vector2(self.game.camera.camera.topleft) - self.pos
        self.rot = direction.angle_to(Vector2(1, 0))
        self.image = pg.transform.rotate(GR.load_image(GR.PLAYER_IMG), self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def draw_health(self, display, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        if pct > 0.6:
            col = GREEN
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        pg.draw.rect(display, col, fill_rect)
        pg.draw.rect(display, WHITE, outline_rect, 2)

    def update(self):
        # Checks where it has to move
        self.__rotate()
        self.__get_keys()
        # Moves in time, not in pixels, independent of our frame rate
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.obstacle, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_walls(self, self.game.obstacle, 'y')
        self.rect.center = self.hit_rect.center
        