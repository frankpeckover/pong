import random
import pygame

class Ball:
    def __init__(self, screen):
        self.screen = screen
        self.xPos = self.screen.get_width() / 2
        self.yPos = self.screen.get_height() * 0.75
        self.xVel = random.choice([-5, -4, -3, -2, 2, 3, 4, 5]) / 5
        self.yVel = -(random.randint(3, 9)) / 5
        self.radius = 5
        self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)
        pass

    def updatePosition(self):
        self.xPos += self.xVel
        self.yPos += self.yVel
        pass

    def flipVelocity(self, vel):
        if vel == 'x':
            self.xVel *= -1
        else:
            self.yVel *= -1
        pass

    def draw(self):
        self.rect.top = self.yPos
        self.rect.left = self.xPos
        pygame.draw.rect(self.screen, (0,0,0), self.rect)
        pass

    def checkBallPos(self):
        if  self.xPos <= 0 or self.xPos >= self.screen.get_width():
            self.flipVelocity('x')
        if self.yPos <= 0:
            self.flipVelocity('y')
        if self.yPos > self.screen.get_height():
            #give some sort of punishment
            self.xPos = 200
            self.yPos = 200
            return False
        return True