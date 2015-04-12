"""This is the view class which is being imported to main.py"""

import pygame
from pygame.locals import *
import random
import math
import time
import numpy as np
import copy

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

        for row in self.model.proposed_board:
            for item in row:
                if item:
                    self.draw_tile(item, item.x, item.y)

        if pygame.font:
            font = pygame.font.Font(None,26)
            text = font.render(" Player %s's turn" % self.model.current_player.name, 1, (255,255,255))
            textpos = text.get_rect(centerx=300,centery=620)
            self.screen.blit(text,textpos)
        pygame.display.update()