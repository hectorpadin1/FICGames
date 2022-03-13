from managers.resourcemanager import ResourceManager as GR
import pygame as pg
from settings import *


class Dialog():

    def __init__(self,dialog_file):
        self.dialog = [("Paco","Me como mi cacota"), ("Juan","Si asi es")]
        self.font = GR.load_font(GR.MAIN_FONT,GUI_FONT_SIZE)

        #Load BG
        self.image = GR.load_image(GR.DIALOG_BG)
        self.rect = self.image.get_rect() 
        self.rect.bottomright = (WIDTH,HEIGHT)

        #Zones
        xbox,ybox = self.rect.topleft
        self.__set_name("Caca",(xbox+25,ybox+20))
        self.start_palabra = 0
        self.palabra = 0
        self.lines=[]
        self.txt_pos_x = xbox+25
        self.txt_pos_y = ybox+45
        self.__load_dialog("Me encanta comer mojones es mi gran pasión.")

        #Pulsa Cualquier tecla
        """
        font1 = GR.load_font(GR.MAIN_FONT,14)
        self.indicacion_surface = font1.render("(Presiona cualquier tecla)", True, (240,240,240))
        self.indicacion_rect = self.indicacion_surface.get_rect()
        xbox,ybox = self.rect.topright
        self.indicacion_rect.topright =(xbox,ybox)
        """

    def __set_name(self,name,pos):
        self.name_surface = self.font.render(name, True, (154,122,37))
        self.name_rect = self.name_surface.get_rect()
        self.name_rect.topleft = pos


    ## RENDERIZARLO POR PALABRAS E
    def __load_dialog(self,frase):
        if self.palabra != -1:
            splited = frase.split()
            render_txt = ' '.join(splited[self.start_palabra:self.palabra])
            print(render_txt)

            #Creamos Nueva línea
            rendered = self.font.render(render_txt, True, (240,240,240))        
            self.dialog_rect = rendered.get_rect()
            #Si sobrepasa creamos nueva línea
            if self.dialog_rect.size[0] > self.rect.size[0]-50:
                render_txt = ' '.join(splited[self.start_palabra:self.palabra-1])
                rendered = self.font.render(render_txt, True, (240,240,240))        
                self.lines.append(rendered)
                self.start_palabra = self.palabra
                print("Sobrepasa")
            else:
                if self.lines == []:
                    self.lines.append(rendered)
                else:
                    self.lines[-1] = rendered


            #Determinamos Si Continuamos o paramos
            if len(splited)-1 < self.palabra:
                self.palabra = -1
            else:
                self.palabra = self.palabra + 1

    def update(self,dt):
        self.__load_dialog("me como mi cacota wei 1 2 3 4 5 6 7 hector feo esto van a ser mas de 2 lienas")
        
    
    def draw(self, display):
        display.blit(self.image, self.rect)
        display.blit(self.name_surface, self.name_rect)
        margin = 0
        for line in self.lines:
            display.blit(line, pg.Rect(self.txt_pos_x,self.txt_pos_y+margin,350,120))
            margin = margin + 25
        #display.blit(self.indicacion_surface, self.indicacion_rect)