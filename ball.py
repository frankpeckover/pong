import random
import pygame

class Ball:
    def __init__(self, screen, speed=1):
        self.speed = speed
        self.screen = screen
        self.screenWidth = self.screen.get_width()
        self.screenHeight = self.screen.get_height()
        self.xPos = self.screenWidth / 2
        self.yPos = self.screenHeight * 0.85
        self.xVel = random.choice([-(random.random() + 0.15), (random.random() + 0.15)])
        self.yVel = -(random.random() + 0.25)
        self.radius = 5
        self.rect = pygame.Rect(self.xPos, self.yPos, self.radius, self.radius)
        pass

    def updatePosition(self):
        self.xPos += self.xVel * self.speed
        self.yPos += self.yVel * self.speed
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
        if  self.xPos <= 60 or self.xPos >= self.screenWidth - 60:
            self.flipVelocity('x')
            return True
        if self.yPos <= 0:
            self.flipVelocity('y')
            return True
        if self.yPos > self.screenHeight:
            #give some sort of punishment
            return False
        return True