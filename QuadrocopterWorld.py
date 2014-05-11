from map import MapGenerator
# from Quadrocopter import Quadrocopter
import Tkinter as tk 
from random import randint, random
import os
import math

class QuadrocopterWorld(tk.Frame):
    def __init__(self, generatedMap, master = None):
    	tk.Frame.__init__(self, master)
    	self.moveStep = 10
    	self.master.bind("<Right>", self.moveRight)
    	self.master.bind("<Left>", self.moveLeft)
    	self.master.bind("<Up>", self.moveUp)
    	self.master.bind("<Down>", self.moveDown)
    	self.map = generatedMap
    	self.master.title("Quadrocopter World")
    	self.canvas = tk.Canvas(self.master, width = self.map.rows * 160, height = self.map.cols * 160)
    	self.canvas.pack()

    def moveRight(self, event):
    	if self.canvas.coords(self.quadrocopterGraphics)[0] <= int(self.map.rows * 160) - self.quadrocopterSize - self.moveStep:
    		self.canvas.move(self.quadrocopterGraphics, self.moveStep, 0)

    def moveLeft(self, event):
    	if self.canvas.coords(self.quadrocopterGraphics)[0] >= self.moveStep:
    		self.canvas.move(self.quadrocopterGraphics, -self.moveStep, 0)

    def moveUp(self, event):
    	if self.canvas.coords(self.quadrocopterGraphics)[1] >= self.moveStep:
    		self.canvas.move(self.quadrocopterGraphics, 0, -self.moveStep)

    def moveDown(self, event):
    	if self.canvas.coords(self.quadrocopterGraphics)[1] <= int(self.map.cols * 160) - self.quadrocopterSize - self.moveStep:
	    	self.canvas.move(self.quadrocopterGraphics, 0, self.moveStep)

    def drawMap(self):
    	colors = ["#FF201A", "#FF301C", "#FF4820", "#FF6126", "#FF792C", "#FF8F32", "#FFA539", "#FFBB3F", "#FFCF46", "#FFE34C"]
    	for i in range(self.map.num_of_bldgs):
		    self.canvas.create_rectangle(self.map.x[i] * 8, self.map.y[i] * 8, self.map.x[i] * 8 + self.map.length[i] * 8, self.map.y[i] * 8 + self.map.width[i] * 8, fill = colors[9 - int(math.floor(self.map.height[i]))]) 

    def drawQuadrocopter(self):
    	self.quadrocopterSize = 20
    	randomY = randint(0, int(self.map.rows * 160 - self.quadrocopterSize));
    	randomX = randint(0, int(self.map.cols * 160 - self.quadrocopterSize));
    	self.quadrocopterGraphics = self.canvas.create_oval(randomX, randomY, randomX + self.quadrocopterSize, randomY + self.quadrocopterSize, outline = 'black', fill = 'gray40', tags = ('quadrocopter'))

if __name__ == "__main__":
	generatedMap = MapGenerator(os.path.dirname(os.path.abspath(__file__)) + "/currentMap.txt", int(5), int(5))
	generatedMap.generate_map()
	quadrocopterWorld = QuadrocopterWorld(generatedMap)
	quadrocopterWorld.drawMap()
	quadrocopterWorld.drawQuadrocopter()
	quadrocopterWorld.mainloop()
	
