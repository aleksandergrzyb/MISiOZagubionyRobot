from Quadrocopter import Quadrocopter
import random
import copy

class ParticleFilter:
    def __init__(self, world):
        self.world = world
        self.particles = []
        self.weights = []

    def createParticles(self, numberOfParticles):
        self.numberOfParticles = numberOfParticles
        for i in range(numberOfParticles):
            particle = Quadrocopter(self.world, 5)
            particle.setNoise(1.0, 0.05)
            self.particles.append(particle)

    def calculateWeights(self, measurement):
        self.weights = []
        for i in range(self.numberOfParticles):
            self.weights.append(self.particles[i].measurementProbability(measurement))
        # print 'Wagi: ' + str(self.weights)
        maximumWeight = max(self.weights)
        for i in range(len(self.weights)):
            self.weights[i] = maximumWeight - self.weights[i]

    def resampleParticles(self, measurement):
        resampledParticles = []
        self.calculateWeights(measurement)
        index = int(random.random() * self.numberOfParticles)
        beta = 0.0
        maximumWeight = max(self.weights)
        for i in range(self.numberOfParticles):
            beta += random.random() * 2.0 * maximumWeight
            while beta > self.weights[index]:
                beta -= self.weights[index]
                index = (index + 1) % self.numberOfParticles
            resampledParticles.append(copy.deepcopy(self.particles[index]))
        # print 'Old: ' + str(self.particles)
        # print 'New: ' + str(resampledParticles)
        self.particles = resampledParticles