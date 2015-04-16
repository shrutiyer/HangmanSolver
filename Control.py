"""Mouse control class"""

import pygame
from pygame.locals import *
import random
import math
import time
import numpy as np
import copy

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
            #if left click -> Select this tile from inventory
                if pygame.mouse.get_pos()[1]> 640 and pygame.mouse.get_pos()[1] < 680:
                    #only select if mouse if hovering on an inventory tile
                    self.model.letter_chosen = self.model.current_player.inventory.letters_inhand[(pygame.mouse.get_pos()[0] -160)/40]
                    self.indexofletterchosen = int((pygame.mouse.get_pos()[0] -160)/40)
                else:
                    print 'Left click to select a tile, right click to place on board'
            if pygame.mouse.get_pressed()[2] and self.model.letter_chosen: #right mouse button
            #if right click -> place chosen tile on spot selected
                #check to see if place is already occupied
                if self.model.board[(pygame.mouse.get_pos()[0])/40, (pygame.mouse.get_pos()[1])/40] == None:
                    self.model.letter_chosen.x = pygame.mouse.get_pos()[0]/40
                    self.model.letter_chosen.x *= 40
                    self.model.letter_chosen.y = pygame.mouse.get_pos()[1]/40
                    self.model.letter_chosen.y *= 40

                    self.model.proposed_positions.append([self.model.letter_chosen.x,self.model.letter_chosen.y])
                    #copy the tile to the board
                    self.model.proposed_board[(pygame.mouse.get_pos()[0])/40, (pygame.mouse.get_pos()[1])/40] = copy.copy(self.model.letter_chosen)
                    
                    #next delete letter chosen from inventory
                    self.model.current_player.inventory.add_placed_tile(self.model.current_player.inventory.letters_inhand[self.indexofletterchosen])
                    self.model.current_player.inventory.letters_inhand.pop(self.indexofletterchosen)
                    self.model.letter_chosen = None #can't use same letter again
            if pygame.mouse.get_pressed()[1]: #middle mouse click
            #if middle click -> end move
                #move complete, refill inventory
                if len(self.model.current_player.inventory.letters_inhand) == 7:
                    #Give up turn, get new tiles
                    for i in range(6):
                        self.model.bag_contents.put_back(self.model.current_player.inventory.letters_inhand[i].letter)
                    del self.model.current_player.inventory.letters_inhand[:]
                    self.model.current_player.inventory.pick_letters(self.model)
                    self.model.turn_number +=1
                else:
                    word = self.model.is_legal()
                    if word != False:
                        del self.model.proposed_positions[:]
                        self.model.current_player.update_score(word)
                        print self.model.current_player.score
                        self.model.current_player.inventory.pick_letters(self.model)
                        self.model.turn_number +=1 
                        self.model.board = self.model.proposed_board.copy()
                    else:
                        self.model.current_player.inventory.letters_inhand.extend(self.model.current_player.inventory.placed_letters)
                        self.model.proposed_board = self.model.board.copy()
                    self.model.proposed_positions = []
                    self.model.proposed_word = ''

                self.model.current_player.inventory.placed_letters = []

