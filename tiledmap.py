import pygame as pg
import pytmx
from settings import *
import sys



class TiledMap:
    def __init__(self, level):
        if level==1:
            tm = pytmx.load_pygame(LEVEL1, pixelalpha=True)
        else:
            print("El mapa no existe")
            sys.exit()
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, 
                                            y * self.tmxdata.tileheight))
    
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


"""


class Map:

    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * SPRITE_BOX
        self.height = self.tileheight * SPRITE_BOX
"""

