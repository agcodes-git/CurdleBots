import pygame, math, random
class node:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.value = 255

    def draw(self, s):
        if self.value == 255: color = (150,255,0)
        else: color = (180,50,180)
        pygame.draw.circle(s,color,(int(self.x),int(self.y)),3,0)
