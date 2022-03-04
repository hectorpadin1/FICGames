import pygame as pg
from sprites.character import Character
from settings import *
from pygame.math import Vector2
from gestorrecursos import GestorRecursos as GR


class Mob(Character):

    def __init__(self, mob_group, x, y, collide_groups):
        super().__init__(mob_group, GR.MOB_IMAGE, MOB_HIT_RECT.copy(), x, y, MOB_HEALTH, collide_groups)
        self.acc = Vector2(0, 0)

    def update(self, player_pos, dt):
        self.rot = (player_pos - self.pos).angle_to(Vector2(1, 0))
        self.acc = Vector2(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * (dt/1000)
        self.pos += self.vel * (dt/1000) + 0.5 * self.acc * (dt/1000) ** 2
        super().update()
    
    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)