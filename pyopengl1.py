import pygame as pg
from OpenGL.GL import *

class App:

    def __init__(self):

        pg.init() #begint pygame
        pg.display.set_mode((640, 400), pg.OPENGL|pg.DOUBLEBUF) #venster aangemaakt, met flags: we gebruiken OpenGL en een 'double buffering' syteem
        self.clock = pg.time.Clock() #klok aangemaakt, om de framerate aan te passen

        glClearColor(1, 0.2, 0.2, 1) #kleur van het scherm (RGBA)
        self.mainLoop()

    def mainLoop(self): #gameloop aangemaakt die altijd runt
        
        running = True
        while (running):

            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False

            glClear(GL_COLOR_BUFFER_BIT) #alle kleurwaardes op het scherm worden gecleared
            pg.display.flip()

            self.clock.tick(60) #framerate
        self.quit()

    def quit(self):

        pg.quit()

if __name__ == "__main__":
    myApp = App()