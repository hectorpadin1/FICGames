import pygame as pg
from sprites.character import Character
from settings import *
from math import pow, sqrt
from pygame.math import Vector2
from sprites.bullet import Bullet
from gestorrecursos import GestorRecursos as GR


class Mob(Character):

    def __init__(self, mob_group, x, y, collide_groups):
        super().__init__(mob_group, GR.MOB_IMAGE, MOB_HIT_RECT.copy(), x, y, MOB_HEALTH, collide_groups)
        self.acc = Vector2(0, 0)
        self.follow = False
        self.last_shot = pg.time.get_ticks()

    def update(self, bullets, rate):
        # Shooting
        if self.follow:
            now = pg.time.get_ticks()
            if now - self.last_shot > rate:
                self.last_shot = now
                Bullet(bullets, self.pos, self.rot)
        super().update()


class MobBasico(Mob):
    
    def update(self, player_pos, bullet, dt):
        distance = sqrt(pow(player_pos.x - self.pos.x, 2) + pow(player_pos.x - self.pos.x, 2))
        if distance > MOB_ATTK_DISTANCE:
            if not self.follow:
                return
            elif distance > MOB_ATTK_DISTANCE*4:
                self.follow = False
                return
        self.follow = True
        self.rot = (player_pos - self.pos).angle_to(Vector2(1, 0))
        if distance > MOB_ATTK_DISTANCE/2:
            self.acc = Vector2(MOB_SPEED, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * (dt/1000)
            self.pos += self.vel * (dt/1000) + 0.5 * self.acc * (dt/1000) ** 2
        super().update(bullet, MOB_BULLET_RATE)
