from random import random, randint
from Tkinter import *

class World:
    def __init__(self, path):
        self.path = path
        self.rows = 0
        self.cols = 0
        self.quadro_x = 0
        self.quadro_y = 0
        self.observed_bldgs = []
        self.observed_centers = []
        self.centers = []
        # sensor distances 1, 2 and 3
        self.range1 = 12
        self.range2 = 25
        self.range3 = 40
        self.sensor_error2 = {"x": 0.5, "y":0.5, "length":0.5, "width":0.5, "height":0.5}
        self.sensor_error3 = {"x": 1.0, "y":1.0, "length":1.0, "width":1.0, "height":1.0}

    def read_map(self):
        self.x = []
        self.y = []
        self.height = []
        self.width = []
        self.length = []
        self.num_of_buildings = 0
        with open(self.path, 'r') as f:
            for line in f:
                params = line.strip().split()
                if len(params) == 1:
                    self.num_of_buildings = int(params[0])
                elif len(params) == 2:
                    print params
                    self.rows = int(params[0])
                    self.cols = int(params[1])
                elif len(params) == 5:
                    self.x.append(float(params[0]))
                    self.y.append(float(params[1]))
                    self.height.append(float(params[2]))
                    self.width.append(float(params[3]))
                    self.length.append(float(params[4]))
        for i in range(self.num_of_buildings):
            self.centers.append([float(self.x[i]+ 0.5*float(self.length[i])), float(self.y[i] + 0.5*float(self.width[i]))])

    def observe(self, x, y):
        # returns list of observed houses within range of 8
        # Manhattan distance
        self.observed_bldgs = []
        for i in range(self.num_of_buildings):
            if abs(self.centers[i][0]-x) + abs(self.centers[i][1]-y) <= self.range1:
                self.observed_bldgs.append(
                    {"number":i, 
                     "x": self.x[i],
                     "y": self.y[i],
                     "height": self.height[i],
                     "width": self.width[i],
                     "length": self.length[i]
                     })
            elif abs(self.centers[i][0]-x) + abs(self.centers[i][1]-y) <= self.range2:
                if self.length[i]<=1 and self.width <= 1:
                    pass
                else:
                    self.observed_bldgs.append(
                    {"number":i, 
                     "x": self.x[i] + self.sensor_error2["x"]*random(),
                     "y": self.y[i] + self.sensor_error2["y"]*random(),
                     "height": self.height[i] + self.sensor_error2["height"]*random(),
                     "width": self.width[i] + self.sensor_error2["width"]*random(),
                     "length": self.length[i] + self.sensor_error2["length"]*random()
                     })
            elif abs(self.centers[i][0]-x) + abs(self.centers[i][1]-y) <= self.range3:
                if self.length[i]<=2 and self.width <= 2:
                    pass
                else:
                    self.observed_bldgs.append(
                    {"number":i, 
                     "x": self.x[i] + self.sensor_error3["x"]*random(),
                     "y": self.y[i] + self.sensor_error3["y"]*random(),
                     "height": self.height[i] + self.sensor_error3["height"]*random(),
                     "width": self.width[i] + self.sensor_error3["width"]*random(),
                     "length": self.length[i] + self.sensor_error3["length"]*random()
                     })
        self.observed_centers = []
        for i in range(len(self.observed_bldgs)):
            self.observed_centers.append([self.observed_bldgs[i]["x"] + 0.5*self.observed_bldgs[i]["length"],
                                          self.observed_bldgs[i]["y"] + 0.5*self.observed_bldgs[i]["width"]]) 
        return self.observed_bldgs, self.observed_centers

    def visualize_observed_buildings(self):
        master = Tk()
        dis = Canvas(master, width=world.rows*160, height=world.cols*160)
        for i in range(len(self.observed_bldgs)):
            dis.create_rectangle(self.observed_bldgs[i]["x"]*8, self.observed_bldgs[i]["y"]*8, 
                     self.observed_bldgs[i]["x"]*8 + self.observed_bldgs[i]["length"]*8, 
                     self.observed_bldgs[i]["y"]*8 + self.observed_bldgs[i]["width"]*8, 
                     fill="blue") 
        dis.pack()
        mainloop()

world = World("/home/jacek/Studia/MISIO/MISiOZagubionyRobot/mapa.txt")
world.read_map()
obs_bldgs, obs_cent = world.observe(0, 0)
print world.centers
print obs_cent
# master = Tk()
# dis = Canvas(master, width=world.rows*160, height=world.cols*160)
# for i in range(len(obs_bldgs)):
#     dis.create_rectangle(obs_bldgs[i]["x"]*8, obs_bldgs[i]["y"]*8, 
#                          obs_bldgs[i]["x"]*8 + obs_bldgs[i]["length"]*8, 
#                          obs_bldgs[i]["y"]*8 + obs_bldgs[i]["width"]*8, 
#                          fill="blue") 
# dis.pack()
# mainloop()
world.visualize_observed_buildings()