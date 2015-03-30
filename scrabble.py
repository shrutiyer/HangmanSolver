# -*- coding: utf-8 -*-
"""
Iteration 1 of our scrabble solver
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
        for x in range(30,630,40):
            for y in range(30,630,40):
                block = Block((255,255,204), 37,37,x,y)
                self.blocks.append(block)

        self.tiles = []
        for x in range(190,470,40):
            tile = Block((255,255,255), 37,37,x,670)
            self.tiles.append(tile)

        self.bag_contents = Bag()

    def update(self):
        """ Update the game state """
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
    def __init__(self):
        self.contents = {'A':12,'B':2,'C':2, 'D':4, 
                        'E':12, 'F': 2, 'G':3, 'H':2, 
                        'I': 9,'J':1, 'K': 1, 'L': 4,
                        'M':2, 'N':6, 'O':8, 'P':2,
                        'Q':1, 'R':6, 'S':4, 'T':6,
                        'U':4,'V':2, 'W':2, 'X':1,
                        'Y':2,'Z':1}
    def makeList(self):
        bag_list = []
        for letter in self.contents:
            for i in range(self.contents[letter]):
                bag_list.append(letter)
        return bag_list

class PyGameWindowView(object):
    """ A view of brick breaker rendered in a Pygame window """
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
        for tile in self.model.tiles:
            pygame.draw.rect(self.screen,
                             pygame.Color(tile.color[0],tile.color[1],tile.color[2]),
                             pygame.Rect(tile.x,tile.y,tile.width,tile.height))
        pygame.display.update()
    
class PyGameController(object):
    """ Handles keyboard input"""
    def __init__(self,model):
        self.model = model
    
    def handle_event(self,event):
        """ Look for left and right keypresses to modify the x velocity of the paddle """
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.paddle.vx += -1.0
        if event.key == pygame.K_RIGHT:
            self.model.paddle.vx += 1.0

if __name__ == '__main__':
    pygame.init()

    size = (650,750)
    screen = pygame.display.set_mode(size)

    model = Model()
    view = PyGameWindowView(model,screen)

    controller = PyGameController(model)

    running = True

    print model.bag_contents.makeList()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)

        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()