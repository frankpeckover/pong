import random
import pygame
from ball import Ball
from paddle import Paddle

class Pong:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen = pygame.display.set_mode([800, 600])
        self.screenWidth = self.screen.get_width()
        self.screenHeight = self.screen.get_height()

        self.population = []
        self.previousPopulation = []
        self.populationSize = 40

        self.createPopulation()
        self.generation = 1

        self.running = True
        self.gameLoop()
        pass

    def createPopulation(self):
        for i in range(self.populationSize):
            paddle = Paddle(self.screen)
            ball = Ball(self.screen)
            self.population.append([paddle, ball
            ])
        pass

    def evaluateFitness(self):
        sum = 0
        for individual in self.previousPopulation:
            sum += individual[0].score 
        for individual in self.previousPopulation:
            individual[0].fitness = individual[0].score / sum
        pass

    def nextGeneration(self):
        self.evaluateFitness()
        for i in range(self.populationSize):
            ball = Ball(self.screen)
            self.population.append([self.matePopulation(), ball])

    def matePopulation(self):
        index = 0
        r = random.random()

        while(r > 0):
            r = r - self.previousPopulation[index][0].fitness
            index += 1
        index -= 1
        paddle = self.previousPopulation[index][0]
        child = Paddle(self.screen, paddle.brain.copy())
        child.brain.mutate(0.1)
        return child

    def update(self):
        if len(self.population) <= 0:
            self.nextGeneration()
            self.generation += 1
            print("Generation: ", self.generation)
        else:
            for individual in self.population:
                paddle = individual[0]
                ball = individual[1]
                paddle.score += 1
                if not ball.checkBallPos():
                    self.previousPopulation.append(self.population.pop(self.population.index(individual)))
                    pass
                ball.updatePosition()
                paddle.collisionCheck(ball)
                prediction = paddle.think([[paddle.pos / self.screenWidth],[ball.xPos / self.screenWidth],[ball.yPos / self.screenHeight], [ball.xVel], [ball.yVel]])
                if prediction == 0:
                    paddle.move(1)
                elif prediction == 2:
                    paddle.move(-1)
                pass

    def draw(self):
        self.screen.fill((255,255,255))
        for individual in self.population:
            paddle = individual[0]
            ball = individual[1]
            paddle.draw()
            ball.draw()
        pass

    def gameLoop(self):
        self.draw()
        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            if (self.generation >= 1):
                self.draw()
            pygame.display.flip()
                


game = Pong()