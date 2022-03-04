import pygame as pg
from sprites.character import Character
from pygame.math import Vector2
from math import cos, pi
from settings import *
from gestorrecursos import GestorRecursos as GR
from soundcontroller import SoundController as SC


class Player(Character):
    #NO ME MOLA NADA COMO SE ESTÁ ACOPLANDO TODO EL JUEGO, MIRAR DE SIMPLEMENTE DAR DE ALTA EL SPRITE
    def __init__(self, x, y, collide_groups):
        super().__init__(None, GR.PLAYER_IMG, PLAYER_HIT_RECT, x, y, PLAYER_HEALTH, collide_groups)
        self.last_shot = 0
        pg.mouse.set_pos((x+10) * SPRITE_BOX, y * SPRITE_BOX)
        self.mouse = pg.mouse.get_pos()
        self.shooting = False
    
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
        # Mirar de cambiar esto
        if keys[pg.K_SPACE]:
            self.shooting = True
        else:
            self.shooting = False
    
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

    def update(self, camera_pos,dt):
        # Checks where it has to move
        direction = pg.mouse.get_pos() - Vector2(camera_pos) - self.pos
        self.rot = direction.angle_to(Vector2(1, 0))
        self.__get_keys()
        # Moves in time, not in pixels, independent of our frame rate
        self.pos += self.vel * (dt/1000)
        super().update()
        