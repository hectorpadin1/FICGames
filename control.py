import pygame as pg

class AbstractControler:

    #abstracta control? -> yo creo k no hace falta
    
    #algo de este rollo
    def up(self):
        return

    def down(self):
        pass

    def right(self):
        pass   

    def left(self):
        pass    

    def reload(self):
        pass

    def isShooting(self):
        pass


class Controler(AbstractControler):

    def up(self):
        return pg.key.get_pressed()[pg.K_w]

    def down(self):
        return pg.key.get_pressed()[pg.K_s]

    def right(self):
        return pg.key.get_pressed()[pg.K_d]   

    def left(self):
        return pg.key.get_pressed()[pg.K_a]    

    def reload(self):
        return pg.key.get_pressed()[pg.K_r]  

    def switchPistol(self):
        if pg.key.get_pressed()[pg.K_1]:
            return 1
        elif pg.key.get_pressed()[pg.K_2]:
            return 2
        elif pg.key.get_pressed()[pg.K_3]:
            return 3
        else:
            return 0

    def isShooting(self):
        return pg.mouse.get_pressed()[0]