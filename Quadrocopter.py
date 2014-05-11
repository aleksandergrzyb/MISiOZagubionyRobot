from math import *
import random

# -------- My world description --------
# World is a square
# World consists of buildings with different heights
# World should be a class that is an array of objects with coordinates and height
# World structure example

world = World()
world.size = 100
world.buildings[i].x = 5
world.buildings[i].y = 10
world.buildings[i].altitude = 100
world.minimumAltitude = 50 # Height of the tallest building
world.maximumAltitude = 100 # Some reasonable number

class Quadrocopter:
    def __init__(self, world):
        self.x = random.random() * world.size
        self.y = random.random() * world.size
        self.altitude = world.minimumAltitude + random.random() * (world.maximumAltitude - world.minimumAltitude)
        self.orientation = random.random() * 2.0 * pi
        self.forwardNoise = 0.0
        self.turnNoise  = 0.0
        self.liftNoise = 0.0
        self.senseNoise   = 0.0
        self.world = world
    
    def set(self, newX, newY, newOrientation, newAltitude):
        if newX < 0 or newX >= self.world.size:
            raise ValueError, 'X coordinate out of bound'
        if newY < 0 or newY >= self.world.size:
            raise ValueError, 'Y coordinate out of bound'
        if newOrientation < 0 or newOrientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        if newAltitude < world.minimumAltitude or newAltitude > world.maximumAltitude:
            raise ValueError, 'Altitude out of bound'

        self.x = float(newX)
        self.y = float(newY)
        self.orientation = float(newOrientation)
        self.altitude = float(newAltitude)
    
    def setNoise(self, newForwardNoise, newTurnNoise, newLiftNoise, newSenseNoise):
        self.forwardNoise = float(newForwardNoise)
        self.turnNoise = float(newTurnNoise)
        self.liftNoise = float(newLiftNoise)
        self.senseNoise = float(newSenseNoise)
    
    def sense(self):
        pass
        # TODO

        # Z = []
        # for i in range(len(landmarks)):
        #     dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
        #     dist += random.gauss(0.0, self.sense_noise)
        #     Z.append(dist)
        # return Z
    
    def move(self, turn, forward):
        pass
        # TODO

        # if forward < 0:
        #     raise ValueError, 'Quadrocopter cant move backwards'         
        
        # # turn, and add randomness to the turning command
        # orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        # orientation %= 2 * pi
        
        # # move, and add randomness to the motion command
        # dist = float(forward) + random.gauss(0.0, self.forward_noise)
        # x = self.x + (cos(orientation) * dist)
        # y = self.y + (sin(orientation) * dist)
        # x %= world_size    # cyclic truncate
        # y %= world_size
        
        # # set particle
        # res = robot()
        # res.set(x, y, orientation)
        # res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        # return res
    
    def gaussian(self, mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    def measurementProbability(self, measurement):
        pass
        # TODO

        # calculates how likely a measurement should be
        # prob = 1.0;
        # for i in range(len(landmarks)):
        #     dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
        #     prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        # return prob

    def __repr__(self):
        return '[x = %.6s y = %.6s orientation = %.6s altitude = %.6s]' % (str(self.x), str(self.y), str(self.orientation), str(self.altitude))

