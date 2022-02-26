import pygame as pg
import sys
import sounds
from settings import *
from gui.button import Button

class StartScreen:

    def __init__(self,display):
        self.display = display #Esto No se yo si estará bien aquí -> revisar patrones
        self.click = False
        self.running = True

    #Eventos Para Cerrar Ventana -> (Está Repetido)
    def events(self):
        for event in pg.event.get():
            #Salir Ventana
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.click = True


    #Dibuja Caja Centrada y Devuelve su tamaño
    def draw_box(self):
        bg = pg.image.load(BOX_BG)
        rect = bg.get_rect()
        rect.center = (WIDTH/2,HEIGHT/2)
        self.display.blit(bg, rect) 
        return rect.size
    
    #Dibuja Logo Centrado con la posibilidad de añadirle un desplazamiento
    def draw_logo(self, dx=0, dy=0):
        logo = pg.image.load(LOGO_IMG)
        rect = logo.get_rect()
        rect.center = (WIDTH/2+dx, HEIGHT/2+dy)
        self.display.blit(logo, rect) 

    def loop(self):
        while self.running:
           
            self.events() 

            #Mouse
            mouse_pos = pg.mouse.get_pos()
      
            #DRAWING
            self.display.fill((66,82,58)) #BG -> Provisional
            _,box_y = self.draw_box()
            self.draw_logo(dy=-((box_y/4)))

            #NOTA: Estamos creando instancias de botón x cada frame, seguramente se pueda optimizar esto si esta clase solo se orienta a la pantalla de carga

            play_btn  = Button(self.display,"Jugar",mouse_pos,self.go_play)
            margin=play_btn.get_size()[1]/2
            stngs_btn = Button(self.display,"Ajustes",mouse_pos,self.go_settings,dy=margin*3)
            exit_btn  = Button(self.display,"Salir",mouse_pos,self.go_exit,dy=margin*6)

            #Ejecutamos Código correspondiete a botones (si procede)
            if self.click:
                for btn in [play_btn,stngs_btn,exit_btn]:
                    if btn.exec_callback(): break
                self.click=False

            pg.display.update() #diferencia conflip?
        return 1
    
    def go_play(self):
        print("play")
        sounds.play_selection()
        self.running=False

    def go_settings(self):
        print("settings")
        sounds.play_selection()

    def go_exit(self):
        pg.quit()
        sys.exit()      

    #IDEA - COSAS DE PEDRO IGNORAR#
    def render_game(self):
        #podríamos pasarle la funcion que renderiza un frame y que la ejecute dentro a la vez que mete elementos de la ui
        pass