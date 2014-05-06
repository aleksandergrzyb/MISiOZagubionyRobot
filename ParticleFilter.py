class ParticleFilter:
    def __init__(self, quadrocopter):
        self.quadrocopter = quadrocopter
        self.particles = []
        self.weights = []

    def createParticles(self, numberOfParticles):
        self.numberOfParticles = numberOfParticles
        for i in range(numberOfParticles):
            quadrocopter = quadrocopter(self.quadrocopter.world)
            quadrocopter.setNoise(0.00, 0.00, 0.00, 0.00)
            self.particles.append(quadrocopter)

    def evaluateAccuracy(self):
        sum = 0.0;
        for i in range(len(self.particles)): # calculate mean error
            dx = (self.particles[i].x - self.quadrocopter.x + (self.quadrocopter.world.size / 2.0)) % self.quadrocopter.world.size - (self.quadrocopter.world.size / 2.0)
            dy = (self.particles[i].y - self.quadrocopter.y + (self.quadrocopter.world.size / 2.0)) % self.quadrocopter.world.size - (self.quadrocopter.world.size / 2.0)
            err = sqrt(dx * dx + dy * dy)
            sum += err
        return sum / float(len(self.particles))

    def calculateWeights(self, measurement):
        for i in range(self.numberOfParticles)
            self.weights.append(self.particles[i].measurementProbability(measurement))

    def resampleParticles(self):
        resampledParticles = []
        index = int(random.random() * self.numberOfParticles)
        beta = 0.0
        maximumWeight = max(self.weights)
        for i in range(self.numberOfParticles):
            beta += random.random() * 2.0 * maximumWeight
            while beta > self.weights[index]:
                beta -= self.weights[index]
                index = (index + 1) % self.numberOfParticles
            resampledParticles.append(self.particles[index])
        self.particles = resampledParticles