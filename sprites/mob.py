import pygame as pg
from settings import *
from pygame.math import Vector2
from sprites.common import collide_with_walls
from sprites.blood import Blood
from gestorrecursos import GestorRecursos as GR


class Mob(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        groups = game.all_sprites, game.mobs
        super().__init__(groups, game.mob_img, MOB_HIT_RECT.copy(), x, y, MOB_HEALTH)
        self.game = game
        self.acc = Vector2(0, 0)

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(Vector2(1, 0))
        self.image = pg.transform.rotate(GR.load_image(GR.MOB_IMAGE), self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = Vector2(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
    
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
    
    def kill(self):
        Blood(self.game.all_sprites, self.pos, 0.5, 0.5, -self.rot-110)
        super().kill()