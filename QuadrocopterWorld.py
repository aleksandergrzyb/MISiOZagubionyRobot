from map import MapGenerator
from Quadrocopter import Quadrocopter
from ParticleFilter import ParticleFilter
import Tkinter as tk 
from random import randint, random
import os
import math

class QuadrocopterWorld(tk.Frame):
    def __init__(self, generatedMap, master = None):
        tk.Frame.__init__(self, master)
        self.moveStep = 10
        self.map = generatedMap
        self.nearestBuildingIndexes = []
        self.quadrocopter = Quadrocopter(generatedMap)
        self.particleFilter = ParticleFilter(generatedMap)
        self.particleFilter.createParticles(300)
        self.master.bind("<Right>", self.moveRight)
        self.master.bind("<Left>", self.moveLeft)
        self.master.bind("<Up>", self.moveUp)
        self.master.bind("<Down>", self.moveDown)
        self.master.title("Quadrocopter World")
        self.canvas = tk.Canvas(self.master, width = self.map.rows * 160, height = self.map.cols * 160)
        self.canvas.pack()

    def moveRight(self, event):
        previousX = self.quadrocopter.x
        self.quadrocopter.move(self.moveStep, True)
        self.canvas.move(self.quadrocopterGraphics, math.fabs(self.quadrocopter.x - previousX), 0)

        for i in range(len(self.particleFilter.particles)):
            previousX = self.particleFilter.particles[i].x
            self.particleFilter.particles[i].move(self.moveStep, True)
            self.canvas.move(self.particlesGraphics[i], math.fabs(self.particleFilter.particles[i].x - previousX), 0)

        self.sense()

    def moveLeft(self, event):
        previousX = self.quadrocopter.x
        self.quadrocopter.move(-self.moveStep, True)
        self.canvas.move(self.quadrocopterGraphics, -math.fabs(self.quadrocopter.x - previousX), 0)

        for i in range(len(self.particleFilter.particles)):
            previousX = self.particleFilter.particles[i].x
            self.particleFilter.particles[i].move(-self.moveStep, True)
            self.canvas.move(self.particlesGraphics[i], -math.fabs(self.particleFilter.particles[i].x - previousX), 0)

        self.sense()

    def moveUp(self, event):
        previousY = self.quadrocopter.y
        self.quadrocopter.move(-self.moveStep, False)
        self.canvas.move(self.quadrocopterGraphics, 0, -math.fabs(self.quadrocopter.y - previousY))

        for i in range(len(self.particleFilter.particles)):
            previousY = self.particleFilter.particles[i].y
            self.particleFilter.particles[i].move(-self.moveStep, False)
            self.canvas.move(self.particlesGraphics[i], 0, -math.fabs(self.particleFilter.particles[i].y - previousY))

        self.sense()

    def moveDown(self, event):
        previousY = self.quadrocopter.y
        self.quadrocopter.move(self.moveStep, False)
        self.canvas.move(self.quadrocopterGraphics, 0, math.fabs(self.quadrocopter.y - previousY))

        for i in range(len(self.particleFilter.particles)):
            previousY = self.particleFilter.particles[i].y
            self.particleFilter.particles[i].move(self.moveStep, False)
            self.canvas.move(self.particlesGraphics[i], 0, math.fabs(self.particleFilter.particles[i].y - previousY))

        self.sense()

    def sense(self):
        # print 'quadro: ' + str(self.quadrocopter)
        # print self.particleFilter.particles


        for i in range(len(self.nearestBuildingIndexes)):
            self.canvas.itemconfig(self.buildingsGraphics[self.nearestBuildingIndexes[i]], fill = self.previousColors[i])
        self.previousColors = []
        self.nearestBuildingIndexes = []
        self.nearestBuildingIndexes, measurement = self.quadrocopter.sense()
        for i in range(len(self.nearestBuildingIndexes)):
            self.previousColors.append(self.canvas.itemcget(self.buildingsGraphics[self.nearestBuildingIndexes[i]], "fill"))
            self.canvas.itemconfig(self.buildingsGraphics[self.nearestBuildingIndexes[i]], fill = "blue")
        self.particleFilter.resampleParticles(measurement)
        self.updateParticles()


    def drawMap(self):
        colors = ["#FF201A", "#FF301C", "#FF4820", "#FF6126", "#FF792C", "#FF8F32", "#FFA539", "#FFBB3F", "#FFCF46", "#FFE34C"]
        self.buildingsGraphics = []
        for i in range(self.map.num_of_bldgs):
            self.buildingsGraphics.append(self.canvas.create_rectangle(self.map.x[i] * 8, self.map.y[i] * 8, self.map.x[i] * 8 + self.map.length[i] * 8, self.map.y[i] * 8 + self.map.width[i] * 8, fill = colors[9 - int(math.floor(self.map.height[i]))], tags = ('map')))

    def drawParticles(self):
        self.particlesGraphics = []
        for i in range(len(self.particleFilter.particles)):
            self.particlesGraphics.append(self.canvas.create_oval(self.particleFilter.particles[i].x, self.particleFilter.particles[i].y, self.particleFilter.particles[i].x + self.particleFilter.particles[i].iconSize, self.particleFilter.particles[i].y + self.particleFilter.particles[i].iconSize, fill = 'gray40', tags = ('particle')))

    def updateParticles(self):
        for i in range(len(self.particlesGraphics)):
            self.canvas.coords(self.particlesGraphics[i], (self.particleFilter.particles[i].x, self.particleFilter.particles[i].y, self.particleFilter.particles[i].x + self.particleFilter.particles[i].iconSize, self.particleFilter.particles[i].y + self.particleFilter.particles[i].iconSize))

    def drawQuadrocopter(self):
        self.quadrocopterGraphics = self.canvas.create_oval(self.quadrocopter.x, self.quadrocopter.y, self.quadrocopter.x + self.quadrocopter.iconSize, self.quadrocopter.y + self.quadrocopter.iconSize, outline = 'black', fill = '#2D8B30', tags = ('quadrocopter'))

if __name__ == "__main__":
    generatedMap = MapGenerator(os.path.dirname(os.path.abspath(__file__)) + "/currentMap.txt", int(2), int(2))
    generatedMap.generate_map()
    quadrocopterWorld = QuadrocopterWorld(generatedMap)
    quadrocopterWorld.drawMap()
    quadrocopterWorld.drawQuadrocopter()
    quadrocopterWorld.drawParticles()
    quadrocopterWorld.mainloop()
    
