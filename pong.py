import numpy.random as nprand
import pygame
from ball import Ball
from paddle import Paddle

class Pong:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen = pygame.display.set_mode([1820, 980])
        self.screenWidth = self.screen.get_width()
        self.screenHeight = self.screen.get_height()

        self.simSpeed = 3

        self.population = []
        self.balls = []
        self.previousPopulation = []
        self.populationSize = 256
        self.averageFitnessHistory = []
        self.maximumScoreHistory = []
        self.maximumHitsHistory = []

        self.createPopulation()
        self.createBalls()
        self.generation = 1

        self.running = True
        self.drawAll = True
        self.gameLoop()
        pass

    def createPopulation(self):
        for i in range(self.populationSize):
            paddle = Paddle(self.screen)
            self.population.append(paddle)
        return self.population

    def createBalls(self):
        for i in range(self.populationSize):
            ball = Ball(self.screen, self.simSpeed)
            self.balls.append(ball)
        return self.balls

    def evaluateFitness(self):
        sumScore = 0
        sumHits = 0
        for paddle in self.previousPopulation:
            sumScore += paddle.timeUnderBall
            sumHits += paddle.ballHits
        for paddle in self.previousPopulation:
            paddle.fitness = ((paddle.timeUnderBall * paddle.ballHits) + (15000  / paddle.distanceFromBall)) ** 2
        pass

    def calculateStatistics(self):
        totalFitness = 0
        maximumScore = 0
        maximumHits = 0
        for paddle in self.previousPopulation:
            if paddle.timeUnderBall > maximumScore:
                maximumScore = paddle.timeUnderBall
            if paddle.ballHits > maximumHits:
                maximumHits = paddle.ballHits
            totalFitness += paddle.fitness
        self.averageFitnessHistory.append(totalFitness/len(self.previousPopulation))
        self.maximumScoreHistory.append(maximumScore)
        self.maximumHitsHistory.append(maximumHits)
        pass 

    #build the next generation
    def nextGeneration(self):
        self.evaluateFitness()
        self.calculateStatistics()
        for i in range(self.populationSize):
            parent1 = self.selectRandomBiasedParent()
            parent2 = self.selectRandomBiasedParent()
            child = self.crossover(parent1, parent2, 1)
            
            # parent1 = self.selectFittestParent()
            # child = self.crossover(parent1, parent1, 1)
            if nprand.random() < 0.75:
                child.brain.mutate(0.1)
            self.population.append(child)
        self.createBalls()
        print("Average Fitness: ", self.averageFitnessHistory[-5:])
        print("Maximum Score: ", self.maximumScoreHistory[-5:])
        print("Maximum Hits: ", self.maximumHitsHistory[-5:])


    def selectRandomBiasedParent(self, k=3):
	# first random selection
        index = nprand.randint(len(self.previousPopulation))
        for i in nprand.randint(0, len(self.previousPopulation), k-1):
            # check if better (e.g. perform a tournament)
            if self.previousPopulation[i].fitness > self.previousPopulation[index].fitness:
                index = i
        return self.previousPopulation[index]

    def selectFittestParent(self):
        maxFitness = 0
        fittestPaddle = self.previousPopulation[0]
        for paddle in self.previousPopulation:
            if paddle.fitness > maxFitness:
                maxFitness = paddle.fitness
                fittestPaddle = paddle
        return fittestPaddle

    def crossover(self, parent1, parent2, crossoverRate):
        child = Paddle(self.screen)
        for layer in range(len(child.brain.layers)):
            for row in range(len(child.brain.layers[layer].weights)):
                for weight in range(len(child.brain.layers[layer].weights[row])):
                    if nprand.random() < crossoverRate:
                        child.brain.layers[layer].weights[row][weight] = parent1.brain.layers[layer].weights[row][weight]
                    else:
                        child.brain.layers[layer].weights[row][weight] = parent2.brain.layers[layer].weights[row][weight]
        return child

    def update(self):
        if len(self.population) <= 0:
            self.nextGeneration()
            self.generation += 1
            self.previousPopulation = []
            print("Generation: ", self.generation)
        else:
            toRemove = []
            for i in range(len(self.population)):
                paddle = self.population[i]
                ball = self.balls[i]
                if not ball.checkBallPos():
                    self.previousPopulation.append(paddle)
                    paddle.distanceFromBall = abs(ball.xPos - paddle.pos)
                    toRemove.append(i)
                ball.updatePosition()
                paddle.collisionCheck(ball)
                prediction = paddle.think([[paddle.pos / self.screenWidth],[ball.xPos / self.screenWidth],[ball.yPos / self.screenHeight], [ball.xVel], [ball.yVel]])
                if prediction == 0:
                    paddle.move(1)
                elif prediction == 2:
                    paddle.move(-1)
                pass
            self.population = [paddle for paddle in self.population if self.population.index(paddle) not in toRemove]
            self.balls = [ball for ball in self.balls if self.balls.index(ball) not in toRemove]
            

    def draw(self):
        self.screen.fill((255,255,255))
        if (self.drawAll):
            for i in range(len(self.population)):
                self.population[i].draw()
                self.balls[i].draw()
        else:
            self.population[-1].draw()
            self.balls[-1].draw()
        pass

    def gameLoop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_2:
                        self.simSpeed = 5 if self.simSpeed >= 4.5 else self.simSpeed + 0.5
                        print(self.simSpeed)
                        for paddle in self.population:
                            paddle.speed = self.simSpeed
                        for ball in self.balls:
                            ball.speed = self.simSpeed
                        pass
                    if event.key == pygame.K_1:
                        self.simSpeed = 0 if self.simSpeed <= 0.5 else self.simSpeed - 0.5
                        print(self.simSpeed)
                        for paddle in self.population:
                            paddle.speed = self.simSpeed
                        for ball in self.balls:
                            ball.speed = self.simSpeed
                    if event.key == pygame.K_r:
                        for ball in self.balls:
                            self.balls = []
                        for paddle in self.population:
                            paddle.distanceFromBall = 500
                            self.previousPopulation.append(paddle)
                            self.population = []

            self.update()
            if (len(self.population) > 0):
                if (self.generation % 1 == 0):
                    self.draw()
            pygame.display.flip()
                


game = Pong()