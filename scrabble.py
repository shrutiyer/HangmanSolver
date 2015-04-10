# -*- coding: utf-8 -*-
"""
Scrabble Solver
Shruti Iyer, Paul Krussel, Meghan Tighe
Soft Des Sp 2015
"""

import pygame
from pygame.locals import *
import random
import math
import time
import numpy as np
import copy

class Model(object):
    """ Encodes the game state """
    def __init__(self):
        self.turn_number = 0
        self.blocks = []
        # these are the blank blocks in the 15 by 15 game board
        for x in range(0,600,40):
            for y in range(0,600,40):
                block = Block((255,255,204), 37,37,x,y)
                self.blocks.append(block)

        self.bag_contents = Bag(self)
        #This initializes a bag with the number of each letter in
        # a game of scrabble

        self.board = np.array([[None]*15]*15)

        # Make the players
        self.players = []
        Shruti = Player(self, 'Shruti')
        self.players.append(Shruti)
        Meghan = Player(self,'Meghan')
        self.players.append(Meghan)
        self.current_player = self.players[0]

        #Keeps track of point value for each letter
        self.points = {'A':1,'B':3,'C':3, 'D':2, 
                        'E':1, 'F': 4, 'G':2, 'H':4, 
                        'I': 1,'J':8, 'K': 5, 'L': 1,
                        'M':3, 'N':1, 'O':1, 'P':3,
                        'Q':10, 'R':1, 'S':1, 'T':1,
                        'U':1,'V':4, 'W':4, 'X':8,
                        'Y':4,'Z':10}


    def update(self):
        """ Update the game state """
        self.current_player = self.players[self.turn_number%len(self.players)]

class Block(object):
    """ Encodes the state of a block in the game """
    def __init__(self,color,height,width,x,y):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y

class Player(object):
    def __init__(self,model,name):
        self.model = model
        self.inventory = Inventory(self.model)
        self.name = name
        self.score = 0

    def update_score(self,letter):
        self.score += self.model.points[letter]


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

    def put_back(self,letter):
        self.contents[letter] +=1

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
            self.letters_inhand.append(LetterTile(letter, letter + ".png", 37, 37, 20, 640))

    def define_coordinates(self, model):
        index = 0
        for item in self.letters_inhand:
            item.x = 160 + index*40
            index += 1

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
        self.model.current_player.inventory.define_coordinates(self.model)

        if self.model.letter_chosen:
            pygame.draw.rect(self.screen, (0,255,0), (self.model.letter_chosen.x-1, self.model.letter_chosen.y-1, 40, 40))

        for block in self.model.blocks: 
            #draw each of the blank blocks in the 15 by 15 game board
            pygame.draw.rect(self.screen,
                             pygame.Color(block.color[0],block.color[1],block.color[2]),
                             pygame.Rect(block.x,block.y,block.width,block.height))

        for tile in self.model.current_player.inventory.letters_inhand:
            #draw each of the actual letters that are in hand
            self.draw_tile(tile,tile.x, tile.y)

        for row in self.model.board:
            for item in row:
                if item:
                    self.draw_tile(item, item.x, item.y)

        if pygame.font:
            font = pygame.font.Font(None,26)
            text = font.render(" Player %s's turn" % self.model.current_player.name, 1, (255,255,255))
            textpos = text.get_rect(centerx=300,centery=620)
            self.screen.blit(text,textpos)
        pygame.display.update()
    
class PyGameController(object):
    """ Handles keyboard input"""
    def __init__(self,model):
        self.model = model
        self.model.letter_chosen = None
        self.current_player = None

    def handle_event(self,event):
        """ Look for left and right keypresses to modify the x velocity of the paddle """

        if event.type != MOUSEBUTTONDOWN:
            return
        else:
            if pygame.mouse.get_pressed()[0]: #left mouse button
                if pygame.mouse.get_pos()[1]> 640 and pygame.mouse.get_pos()[1] < 680:
                    #only select if mouse if hovering on an inventory tile
                    self.model.letter_chosen = self.model.current_player.inventory.letters_inhand[(pygame.mouse.get_pos()[0] -160)/40]
                    self.indexofletterchosen = int((pygame.mouse.get_pos()[0] -160)/40)
                else:
                    print 'Left click to select a tile, right click to place on board'
            if pygame.mouse.get_pressed()[2] and self.model.letter_chosen: #right mouse button
                #check to see if place is already occupied
                if self.model.board[(pygame.mouse.get_pos()[0])/40, (pygame.mouse.get_pos()[1])/40] == None:
                    self.model.letter_chosen.x = pygame.mouse.get_pos()[0]/40
                    self.model.letter_chosen.x *= 40
                    self.model.letter_chosen.y = pygame.mouse.get_pos()[1]/40
                    self.model.letter_chosen.y *= 40

                    #copy the tile to the board
                    self.model.board[(pygame.mouse.get_pos()[0])/40, (pygame.mouse.get_pos()[1])/40] = copy.copy(self.model.letter_chosen)
                    
                    #next delete letter chosen from inventory
                    self.model.current_player.inventory.letters_inhand.pop(self.indexofletterchosen)
                    self.model.letter_chosen = None #can't use same letter again
            if pygame.mouse.get_pressed()[1]: #middle mouse click
                #move complete, refill inventory
                if len(self.model.current_player.inventory.letters_inhand) == 7:
                    #Give up turn, get new tiles
                    for i in range(6):
                        self.model.bag_contents.put_back(self.model.current_player.inventory.letters_inhand[i].letter)
                    del self.model.current_player.inventory.letters_inhand[:]
                self.model.current_player.inventory.pick_letters(self.model)
                self.model.turn_number +=1
                

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