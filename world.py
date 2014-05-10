from random import random, randint, seed
from Tkinter import *
from math import sqrt

class World:
    def __init__(self, path):
        self.path = path
        self.rows = 0
        self.cols = 0
        self.quadro_x = 0
        self.quadro_y = 0
        self.observed_bldgs = []
        self.observed_centers = []
        self.quadro_obs_bldgs = []
        self.quadro_obs_centers = []
        self.centers = []
        # sensor distances 1, 2 and 3
        self.range1 = 4
        self.range2 = 6
        self.range3 = 8
        # error max for different distances
        self.sensor_error2 = {"x": 2.0, "y":2.0, "length":2.0, "width":2.0, "height":2.0}
        self.sensor_error3 = {"x": 4.0, "y":4.0, "length":4.0, "width":4.0, "height":4.0}
        self.dist_punishment = 1.0
        self.height_punishment = 2.0

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
            self.centers.append({"x":float(self.x[i]+ 0.5*float(self.length[i])), "y":float(self.y[i] + 0.5*float(self.width[i]))})

    def observe(self, x, y):
        # returns list of observed houses within range of 8
        # Euclidian distance
        self.observed_bldgs = []
        for i in range(self.num_of_buildings):
            if sqrt(pow(self.centers[i]["x"]-x, 2.0) + pow(self.centers[i]["y"]-y, 2)) <= self.range1:
                # Here you can see everything as it is
                self.observed_bldgs.append(
                    {"number":i, 
                     "x": self.x[i],
                     "y": self.y[i],
                     "height": self.height[i],
                     "width": self.width[i],
                     "length": self.length[i]
                     })
            elif  self.range1 < sqrt(pow(self.centers[i]["x"]-x, 2.0) + pow(self.centers[i]["y"]-y, 2)) <= self.range2:
                if self.length[i]<=1 and self.width <= 1:
                    # small buidlings are not visible
                    pass
                else:
                    # everything is shifted and blurred
                    self.observed_bldgs.append(
                    {"number":i, 
                     "x": self.x[i] + self.sensor_error2["x"]*random() - self.sensor_error2["x"]*0.5,
                     "y": self.y[i] + self.sensor_error2["y"]*random() - self.sensor_error2["y"]*0.5,
                     "height": self.height[i] + self.sensor_error2["height"]*random() - self.sensor_error2["height"]*0.5,
                     "width": self.width[i] + self.sensor_error2["width"]*random() - self.sensor_error2["width"]*0.5,
                     "length": self.length[i] + self.sensor_error2["length"]*random() - self.sensor_error2["length"]*0.5
                     })
            elif self.range2 < sqrt(pow(self.centers[i]["x"]-x, 2.0) + pow(self.centers[i]["y"]-y, 2)) <= self.range3:
                if self.length[i]<=2 and self.width <= 2:
                    pass
                else:
                    self.observed_bldgs.append(
                    {"number":i, 
                     "x": self.x[i] + self.sensor_error3["x"]*random() - self.sensor_error3["x"]*0.5,
                     "y": self.y[i] + self.sensor_error3["y"]*random() - self.sensor_error3["y"]*0.5,
                     "height": self.height[i] + self.sensor_error3["height"]*random() - self.sensor_error3["height"]*0.5,
                     "width": self.width[i] + self.sensor_error3["width"]*random() - self.sensor_error3["width"]*0.5,
                     "length": self.length[i] + self.sensor_error3["length"]*random() - self.sensor_error3["length"]*0.5
                     })
        self.observed_centers = []
        for i in range(len(self.observed_bldgs)):
            self.observed_centers.append({"x":self.observed_bldgs[i]["x"] + 0.5*self.observed_bldgs[i]["length"],
                                          "y":self.observed_bldgs[i]["y"] + 0.5*self.observed_bldgs[i]["width"]}) 
        return self.observed_bldgs, self.observed_centers

    def quadro_observe(self):
        # Relative locations of buildings and their centres to the quadrocopter
        self.quadro_obs_bldgs, self.quadro_obs_centers = self.observe(self.quadro_x, self.quadro_y)
        for bldg in self.quadro_obs_bldgs:
            bldg["x"] -= self.quadro_x
            bldg["y"] -= self.quadro_y
        for center in self.quadro_obs_centers:
            center["x"] -= self.quadro_x
            center["y"] -= self.quadro_y 

    # find nearest building seen by the quadrocopter
    # calculate error based on distance to the nearest buidling and 
    # difference in heights
    # WARNING Use quadro_observe before running for get_error for particles
    def get_error(self, x, y):
        # make an observation
        observed_bldgs, observed_centers = self.observe(x, y)
        # Calculate relative distance to buildings and their centers
        for bldg in observed_bldgs:
            bldg["x"] -= x
            bldg["y"] -= y
        for center in observed_centers:
            center["x"] -= x
            center["y"] -= y
        # find nearest building
        for i in range(len(observed_centers)):
            distance = 99999.0
            nearest_bldg = 0
            error = 0.0
            #calculate euclides distance to nearest building seen by quadro and identify it
            for a in range(len(self.quadro_obs_bldgs)):
                temp = pow(observed_centers[i]["x"]-self.quadro_obs_centers[a]["x"], 2.0)\
                     + pow(observed_centers[i]["y"]-self.quadro_obs_centers[a]["y"], 2.0)     
                if temp < distance:
                    distance = temp
                    nearest_bldg = a
            error += distance*self.dist_punishment + pow(observed_bldgs[i]["height"]-self.quadro_obs_bldgs[nearest_bldg]["height"], 2.0)*self.height_punishment
            # When particle is on edge, less buildings are visible
            # This promotes measurements with many buildings visible
            error = error / pow(len(observed_bldgs), 2.0)
            # error = error / len(observed_bldgs)
        return error*10000.0 

    def visualize_observed_buildings(self):
        master = Tk()
        dis = Canvas(master, width=world.rows*160, height=world.cols*160)
        print self.observed_bldgs
        for i in range(len(self.observed_bldgs)):
            dis.create_rectangle(self.observed_bldgs[i]["x"]*8, self.observed_bldgs[i]["y"]*8, 
                     self.observed_bldgs[i]["x"]*8 + self.observed_bldgs[i]["length"]*8, 
                     self.observed_bldgs[i]["y"]*8 + self.observed_bldgs[i]["width"]*8, 
                     fill="blue")
        dis.pack()
        mainloop()

seed()

world = World("/home/jacek/Studia/MISIO/MISiOZagubionyRobot/mapa.txt")
world.read_map()

world.quadro_x = 4.0
world.quadro_y = 4.0
world.quadro_observe()

for i in range(20):
    s = ''
    for j in range(20):
        s += str('%d ' % world.get_error(float(i), float(j)))
    print (s + '\n')

#world.visualize_observed_buildings()