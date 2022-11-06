import pygame
import numpy as np

from neuralNetwork.neuralNetwork import NeuralNetwork

class Paddle:
    def __init__(self, screen, brain=None, speed=1):
        if brain is not None:
            self.brain = brain
        else:
            self.brain = NeuralNetwork([5, 10, 3])
        self.screen = screen
        self.fitness = 0
        self.score = 0
        self.hits = 0
        self.width = 50
        self.height = 10
        self.pos = 0
        self.speed = speed * 2
        self.xUpperLimit = screen.get_width()
        self.xLowerLimit = 0
        self.rect = pygame.Rect(self.pos, self.screen.get_height() - self.height, self.width, self.height)
        pass

    def move(self, direction):
        if self.pos <= self.xUpperLimit - self.width and self.pos >= self.xLowerLimit:
            self.pos += self.speed * direction
        pass

    def think(self, inputs):
        output = self.brain.propagateForward(inputs)
        prediction =  np.argmax(output[-1])
        return prediction

    def draw(self):
        self.rect.left = self.pos
        pygame.draw.rect(self.screen, (0,0,0), self.rect)
        pass

    def collisionCheck(self, ball):
        if ball.xPos > self.pos and ball.xPos < self.pos + self.width:
            if ball.yPos >= self.screen.get_height() - self.height:
                ball.yPos -= (self.height / 2)
                ball.flipVelocity('y')
                self.hits += 1
                return True
        return False
        