from math import *
import random
from random import randint
import copy

class Quadrocopter:
    def __init__(self, world, iconSize = 20):
        self.iconSize = iconSize
        self.altitude = 15
        self.world = world
        self.x = randint(0, int(self.world.rows * 160 - self.iconSize));
        self.y = randint(0, int(self.world.cols * 160 - self.iconSize));
        self.moveNoise = 0.05
        self.senseNoise = 0.05

    def set(self, newX, newY):
        if newX < 0 or newX >= self.world.size:
            raise ValueError, 'X coordinate out of bound'
        if newY < 0 or newY >= self.world.size:
            raise ValueError, 'Y coordinate out of bound'
        self.x = float(newX)
        self.y = float(newY)
    
    def setNoise(self, newMoveNoise, newSenseNoise):
        self.moveNoise = float(newMoveNoise)
        self.senseNoise = float(newSenseNoise)
    
    def sense(self):
        measurementWithNoise = []
        distancesFromAllBuildings = []
        for i in range(self.world.num_of_bldgs):
            distance = sqrt((self.x - self.world.centerX[i] * 8) ** 2 + (self.y - self.world.centerY[i] * 8) ** 2 + (self.altitude - self.world.height[i]) ** 2)
            distancesFromAllBuildings.append(distance)
        distancesFromAllBuildingsCopy = copy.deepcopy(distancesFromAllBuildings)
        distancesFromAllBuildings.sort()
        nearestBuildings = distancesFromAllBuildings[0:4]
        nearestBuildingIndexes = []
        for i in range(len(nearestBuildings)):
            nearestBuildingIndexes.append(distancesFromAllBuildingsCopy.index(nearestBuildings[i]))
            measurementWithNoise.append(nearestBuildings[i] + random.gauss(0.0, self.senseNoise))
        return nearestBuildingIndexes, measurementWithNoise
    
    def move(self, distance, horizontalMove):
        if horizontalMove:
            self.x += float(distance) + random.gauss(0.0, self.moveNoise)
        else:
            self.y += float(distance) + random.gauss(0.0, self.moveNoise)

    def Gaussian(self, mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    def measurementProbability(self, measurement):
        probability = 1.0
        distancesFromAllBuildings = []
        for i in range(self.world.num_of_bldgs):
            distance = sqrt((self.x - self.world.centerX[i] * 8) ** 2 + (self.y - self.world.centerY[i] * 8) ** 2 + (self.altitude - self.world.height[i]) ** 2)
            distancesFromAllBuildings.append(distance)
        distancesFromAllBuildings.sort()
        nearestBuildings = distancesFromAllBuildings[0:4]
        # print 'nearestBuildings: ' + str(nearestBuildings)
        # print 'measurement: ' + str(measurement)
        error = 0.0
        for i in range(len(nearestBuildings)):
            error += fabs(nearestBuildings[i] - measurement[i])

        # for i in range(len(nearestBuildings)):
        #     probability *= self.Gaussian(nearestBuildings[i], self.senseNoise, measurement[i])
            # print 'Probability: ' + str(probability)
        return error

    def __repr__(self):
        return '[x = %.6s y = %.6s]' % (str(self.x), str(self.y))

