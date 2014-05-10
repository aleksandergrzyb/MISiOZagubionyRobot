from random import random, randint

class World:
    def __init__(self, path):
        self.path = path
        self.rows = 0
        self.cols = 0
        self.quadro_x = 0
        self.quadro_y = 0
        self.observed_bldgs = []
        self.centers = []

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
                    self.x.append(int(params[0]))
                    self.y.append(int(params[1]))
                    self.height.append(int(params[2]))
                    self.width.append(int(params[3]))
                    self.length.append(int(params[4]))
        for i in range(self.num_of_buildings):
            self.centers.append([float(self.x[i]+ 0.5*float(self.length[i])), float(self.y[i] + 0.5*float(self.width[i]))])
        print self.centers 

    def observe(self):
        for i in range(self.num_of_buildings):
            pass


world = World("/home/jacek/Studia/MISIO/MISiOZagubionyRobot/mapa.txt")
world.read_map()