import pygame as pg
from sprites.character import Character
from pygame.math import Vector2
from settings import *
from math import cos, pi
from sprites.bullet import Bullet
from control import Controler
from sprites.gun import AbstractGun
from gestorrecursos import GestorRecursos as GR


class Player(Character):
    #NO ME MOLA NADA COMO SE ESTÁ ACOPLANDO TODO EL JUEGO, MIRAR DE SIMPLEMENTE DAR DE ALTA EL SPRITE
    def __init__(self, x, y, bullets, collide_groups):
        super().__init__(None, GR.PLAYER_IMG, PLAYER_HIT_RECT, x, y, PLAYER_HEALTH, collide_groups)
        self.last_shot = 0
        pg.mouse.set_pos((x+10) * SPRITE_BOX, y * SPRITE_BOX)
        self.mouse = pg.mouse.get_pos()
        self.controler = Controler()
        self.guns = [AbstractGun(bullets, 30, GR.BULLET_IMG, 10*FPS)]
        self.gunSelector = 0
        self.shooting = False
    
    # Esto no tiene que estar aquí 
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


    def __callControler(self):
        # Player dynamics
        self.rot_speed = 0
        self.vel = Vector2(0, 0)
        # On-Axis movements
        if self.controler.left():
            self.vel.x = -PLAYER_SPEED
        if self.controler.right():
            self.vel.x = PLAYER_SPEED
        if self.controler.up():
            self.vel.y = -PLAYER_SPEED
        if self.controler.down():
            self.vel.y = PLAYER_SPEED
        # Oposite movements
        if self.controler.left() and self.controler.right():
            self.vel.x = 0
        if self.controler.up() and self.controler.down():
            self.vel.y = 0
        # Diagonal movements        
        if self.vel.x!=0 and self.vel.y!=0:
            self.vel *= cos(pi/4)
        # Shooting
        if (self.controler.isShooting()):
            self.guns[self.gunSelector].shoot()


    def update(self, camera_pos, bullets, dt):
        self.__callControler()
        # Checks where it has to move
        direction = pg.mouse.get_pos() - Vector2(camera_pos) - self.pos
        self.rot = direction.angle_to(Vector2(1, 0))
        # Moves in time, not in pixels, independent of our frame rate
        self.pos += self.vel * (dt/1000)
        super().update()
        # Shooting
        #if self.shooting:
        #    now = pg.time.get_ticks()
        #    if now - self.last_shot > BULLET_RATE:
        #        self.last_shot = now
        #        Bullet(bullets, self.pos, self.rot)
        