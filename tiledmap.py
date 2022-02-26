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

