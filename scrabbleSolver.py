# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29
Based on block Breaker starter code
"""

import pygame
from pygame.locals import *
import random
import math
import time

class Model(object):
    """ Encodes the game state """
    def __init__(self):
        self.blocks = []
        for x in range(30,20,330):
            for y in range(30,20,330):
                block = Block((random.randint(0,255),
                               random.randint(0,255),
                               random.randint(0,255)),15,15,x,y)
                self.blocks.append(block)

    def update(self):
        """ Update the game state (currently only tracking the paddle) """
        pass

class Player(object):
    """ Encodes the state of a block in the game """
    def __init__(self,color,height,width,x,y):
        pass

class Block(object):
    """ Encodes the state of a block in the game """
    def __init__(self,color,height,width,x,y):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y

class Bag(object):
    """This is where the letters stay if not yet used"""
    def __init__(self):
        pass

class PyGameWindowView(object):
    """ A view of block breaker rendered in a Pygame window """
    def __init__(self,model,screen):
        """ Initialize the view with a reference to the model and the screen
            to use for rendering the view """
        self.model = model
        self.screen = screen
        
    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(0,0,0))
        for block in self.model.blocks:
            pygame.draw.rect(self.screen,
                             pygame.Color(block.color[0],block.color[1],block.color[2]),
                             pygame.Rect(block.x,block.y,block.width,block.height))
        pygame.display.update()

class PyGameController(object):
    """ A controller that uses the mosue to move the paddle """
    def __init__(self,model):
        self.model = model
    
    def handle_event(self,event):
        """ Handle the mouse event to have the paddle track the mouse position """


if __name__ == '__main__':
    pygame.init()

    size = (640,480)
    screen = pygame.display.set_mode(size)

    model = Model()
    view = PyGameWindowView(model,screen)

    controller = PyGameController(model)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)

        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()