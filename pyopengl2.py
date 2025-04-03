import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader

class App:

    def __init__(self):

        #initialisatie pygame
        pg.init() #begint pygame
        pg.display.set_mode((1280, 720), pg.OPENGL|pg.DOUBLEBUF) #venster aangemaakt, met flags: we gebruiken OpenGL en een 'double buffering' syteem
        self.clock = pg.time.Clock() #klok aangemaakt, om de framerate aan te passen

        #initialisatie OpenGL
        glClearColor(0, 0, 0.2, 1) #kleur van het scherm (RGBA)
        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt") #parameters van de createShader functie
        glUseProgram(self.shader)
        self.triangle = Triangle()
        self.mainLoop()

    #shaders aanmaken met een createShader functie
    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath, 'r') as f: #de resource runt alleen tijdens de indentation
            vertex_src = f.readlines() #alle inhoud ==> 1 string

        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER), #welke string - welke soort shader
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def mainLoop(self): #gameloop aangemaakt die altijd runt
        
        running = True
        while (running):

            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False

            glClear(GL_COLOR_BUFFER_BIT) #alle kleurwaardes op het scherm worden gecleared
            
            glUseProgram(self.shader)
            glBindVertexArray(self.triangle.vao) #triangle selecteren om te tekenen
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count) #drawmode - vanaf welke waarde beginnen met tekenen - hoeveel vertices tekenen
            
            pg.display.flip()

            self.clock.tick(60) #framerate
        self.quit()

    def quit(self):

        self.triangle.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Triangle:

    def __init__(self):
    
        #de punten van een vorm zoals een driehoek, met x, y, z waardes en rgb waardes
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, #linksonder, rood
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0, #rechtsonder, groen
            0.0,  0.5, 0.0, 0.0, 0.0, 1.0 #midden boven, blauw
        )

        self.vertices = np.array(self.vertices, dtype=np.float32) #vertices worden omgezet naar een 32bit numpy array, zodat de GPU de data kan lezen

        self.vertex_count = 3

        self.vao = glGenVertexArrays(1) #geeft aan op welke manier de data gelezen moet worden als array: eerst de xyz waardes, dan de rgb waardes
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1) #1 vertexbufferobject wordt aangemaakt 
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) #wanneer het over GL_ARRAY_BUFFER gaat, wordt self.vbo bedoeld
        #waar willen we de data laden - hoeveel bytes zijn het - de data zelf - op welke manier laden we de data
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW) #met static draw wordt de data 1 keer gelezen en daarna 60 keer/s neergezet

        glEnableVertexAttribArray(0) #eerste attribute, oftewel positie
        #attribute 0 - 3 waardes - datatype = float - normalise waardes = false - stride: 6 waardes * 4 bytes = 24 - offset: moet je verderop beginnen met waardes lezen? nee
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1) #tweede attribute, oftewel kleur
        #attribute 1 - 3 waardes - datatype = float - normalise waardes = false - stride: 6 waardes * 4 bytes = 24
        #moet je verderop beginnen met waardes lezen? ja, dus offset = 3 waardes * 4 bytes = 12
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    #het werkgeheugen dat aan de GPU wordt gegeven clearen
    def destroy(self):

        glDeleteVertexArrays(1, (self.vao,)) #komma na de variable nodig om aan te geven dat de haakjes een lijst aangeven
        glDeleteBuffers(1, (self.vbo,))

if __name__ == "__main__":
    myApp = App()