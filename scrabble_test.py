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
        # these are the blank blocks in the 15 by 15 game board
        for x in range(0,600,40):
            for y in range(0,600,40):
                block = Block((255,255,204), 37,37,x,y)
                self.blocks.append(block)
        print self.blocks
        self.bag_contents = Bag(self)
        #This initializes a bag with the number of each letter in
        # a game of scrabble

        self.letter_tiles = Inventory(self)
        # All letters once picked from bag
        # don't have to be on board yet


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
    def __init__(self,model):
        self.model = model
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

    def pickTile(self):
        random_letter = random.choice(self.model.bag_contents.makeList())
        self.contents[random_letter] -= 1
        return random_letter

class Inventory(object):
    def __init__(self,model):
        self.letters_inhand = []
        self.model = model
        self.pick_letters(self.model)


    def count_tiles(self,model):
        return 7-len(self.letters_inhand)

    def pick_letters(self,model):
        for i in range(self.count_tiles(model)):
            letter = self.model.bag_contents.pickTile()
            self.letters_inhand.append(LetterTile(letter, letter + ".png", 37, 37, 20, 20))

class LetterTile(object):
    def __init__(self, letter, img_location, height, width, x, y):
        self.height = height
        self.width = width
        self.color = (255,255,240)
        self.x = x
        self.y = y
        self.letter = letter
        self.points = 0 #CHANGE THIS
        self.image = pygame.image.load(img_location)
        self.image_rect = self.image.get_rect()

class PyGameWindowView(object):
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self,model,screen):
        """ Initialize the view with a reference to the model and the screen
            to use for rendering the view """
        self.model = model
        self.screen = screen
        
    def draw_tile(self,tile,x,y):
        square = pygame.draw.rect(self.screen,pygame.Color(0,0,0),pygame.Rect(x,y,37,37))
        self.screen.blit(tile.image,square)

    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(0,0,0))
        for block in self.model.blocks: 
            #draw each of the blank blocks in the 15 by 15 game board
            pygame.draw.rect(self.screen,
                             pygame.Color(block.color[0],block.color[1],block.color[2]),
                             pygame.Rect(block.x,block.y,block.width,block.height))
        index = 0
        for tile in self.model.letter_tiles.letters_inhand:
            #draw each of the actual letters that are already placed on the board
            self.draw_tile(tile,160 + (index * 40),640)
            index +=1
        pygame.display.update()
    
class PyGameController(object):
    """ Handles keyboard input"""
    def __init__(self,model):
        self.model = model
        self.letter_chosen = None

    def handle_event(self,event):
        """ Look for left and right keypresses to modify the x velocity of the paddle """
        
        for event in pygame.event.get()
        if event.type != MOUSEBUTTONDOWN:
            return
        else:
            if pygame.mouse.get_pressed()[0]: #left mouse button
                #highlight the tile
                self.mouse_position = (pygame.mouse_pos[0])
                self.letter_chosen = 
            if 

if __name__ == '__main__':
    pygame.init()

    size = (600,700)
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