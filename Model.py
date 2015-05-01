"""This is the model class along with the other smaller class
This is being imported to the main.py file
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

        self.board = np.array([[None]*15]*15) #this is the real board
        self.proposed_board = self.board.copy() #this is the board if the move being made is implemented
        self.proposed_positions = []
        self.proposed_word = ''

        # Make the players
        self.players = []
        Shruti = Player(self, 'Shruti')
        self.players.append(Shruti)
        Richard = Player(self, 'Richard')
        self.players.append(Richard)
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

    def is_legal(self):
        '''Returns true if move is legal'''
        is_row = self.same_row()
        is_column = self.same_column()
        if not(self.same_row() or self.same_column()):
            print 'not same row or column'
            return False

        if is_row and is_column:
            if self.do_row_stuff():
                is_good_word_length = 0
                if self.turn_number != 0 and len(self.proposed_word) <= len(self.current_player.inventory.placed_letters):
                    is_good_word_length += 1
                row_word = self.proposed_word
                if self.do_column_stuff():
                    if self.turn_number != 0 and len(self.proposed_word) <= len(self.current_player.inventory.placed_letters):
                        is_good_word_length += 1
                    elif is_good_word_length < 2:
                        column_word = self.proposed_word
                        self.proposed_word = row_word + column_word
                        return self.proposed_word
                    else:
                        return False
                else:
                    return False
            else:
                return False

        if is_row:
            print "is_row"
            if self.do_row_stuff():
                if self.turn_number != 0 and len(self.proposed_word) <= len(self.current_player.inventory.placed_letters):
                    return False
                else:
                    return self.proposed_word
            else:
                return False
        else:
            print "is_column"
            if self.do_column_stuff():
                if self.turn_number != 0 and len(self.proposed_word) <= len(self.current_player.inventory.placed_letters):
                    return False
                else:
                    return self.proposed_word
            else:
                return False
            
    def do_column_stuff(self):
        column_number = self.proposed_positions[0][0]/40
        first_row = self.proposed_positions[0][1]/40
        last_row = self.proposed_positions[-1][1]/40

        if self.legal_column_spot(first_row, last_row, column_number):
            while first_row>=0 and self.proposed_board[column_number,first_row] != None:
                 first_row -=1
            while last_row<=14 and self.proposed_board[column_number,last_row] != None:
                last_row +=1
            first_row +=1
            last_row -=1
            for letter in self.proposed_board[column_number,first_row:last_row+1]:
                self.proposed_word += letter.letter
            if self.is_real_word(self.proposed_word):
                return self.proposed_word
            else:
                print self.proposed_word, 'is not a real word'
                return False
        else:
                print 'illegal column spot'
                return False
    
    def do_row_stuff(self):
        row_number = self.proposed_positions[0][1]/40
        first_column = self.proposed_positions[0][0]/40
        last_column = self.proposed_positions[-1][0]/40

        if self.legal_row_spot(first_column, last_column, row_number):
            while first_column >= 0 and self.proposed_board[first_column,row_number] != None:
                first_column -=1
            while last_column <=14 and self.proposed_board[last_column,row_number] != None:
                last_column +=1
            first_column += 1
            last_column -=1
            for letter in self.proposed_board[first_column:last_column+1,row_number]:
                self.proposed_word += letter.letter
            if self.is_real_word(self.proposed_word) and self.legal_row_spot(first_column, last_column, row_number):
                return self.proposed_word
            elif not self.same_column():
                print self.proposed_word, 'is not a real word'
                return False
            # else:
            #     self.proposed_word = ''
            #     return self.do_column_stuff()
            else:
                return False
        else:
            print 'illegal row spot'
            return False

    def is_real_word(self,word):
        word_list = [line.strip() for line in open("words.txt", 'r')]
        return word.lower() in word_list

    def same_row(self):
        '''Returns true if proposed positions are in same row'''
        ref_y = self.proposed_positions[0][1]
        for coordinate in self.proposed_positions:
            if coordinate[1] != ref_y:
                return False
        return True

    def same_column(self):
        '''Returns true if proposed positions are in same column'''
        ref_x = self.proposed_positions[0][0]
        for coordinate in self.proposed_positions:
            if coordinate[0] != ref_x:
                return False
        return True

    def legal_row_spot(self, first_column, last_column, row_number):
        '''Checks to see that words uses at least one tile already on board'''
        for spot in self.proposed_board[first_column:last_column, row_number]:
            if spot == None:
                return False
        return True

    def legal_column_spot(self, first_row, last_row, column_number):
        '''Checks to see that words uses at least one tile already on board'''
        for spot in self.proposed_board[column_number, first_row:last_row]:
            if spot == None:
                return False
        return True

    "###### START OF AI STUFF ######"

    def find_spots(self):
        '''Finds places on the board to put down words'''
        self.players[0].open_spots = []
        for x in range(0,15):
            for y in range(0,15):
                spot = self.board.item((x,y))
                if spot != None:
                    self.players[0].open_spots.append([spot.letter]) 
                    self.ai_check_row(x,y)
                    self.ai_check_column(x,y)
                    #print "spot x and y are ", x, y
                    if self.players[0].open_spots[-1][1] == [0,0] and self.players[0].open_spots[-1][2] == [0,0]:
                        del self.players[0].open_spots[-1]
                    #print self.players[0].open_spots


    def ai_check_row(self, x, y):
        """Will check the row for None and then return a tuple of the letter(s) 
        and the number of spaces available
        left and right spots are number of open spots in both places
        """
        left_spots = 0
        right_spots = 0
        while -1<x-(left_spots+1):
            #print "in first while loop"
            if self.board.item((x-(left_spots+1),y)) == None:
                left_spots += 1
                if self.board.item((x-(left_spots),y-1)) != None or self.board.item((x-(left_spots),y+1)) != None:
                    left_spots -= 1
                    break               
            elif left_spots == 0:
                break
            else:
                left_spots -= 1
                break
        while x+(right_spots+1)<15:
            #print "in second while loop"
            if self.board.item((x+(right_spots+1),y)) == None:
                right_spots += 1
                if self.board.item((x+(right_spots),y-1)) != None or self.board.item((x+(right_spots),y+1)) != None:
                    right_spots -= 1
                    break
            elif right_spots == 0:
                break
            else:
                right_spots -= 1
                break
        self.players[0].open_spots[-1].append([left_spots,right_spots])

    def ai_check_column(self, x, y):
        up_spots = 0
        down_spots = 0
        while -1<y-(up_spots+1):
            #print "in first column while loop"
            if self.board.item((x,y-(up_spots+1))) == None:
                up_spots += 1
                if self.board.item((x-1,y-(up_spots))) != None or self.board.item((x+1,y-(up_spots))) != None:
                    up_spots -= 1
                    break               
            elif up_spots == 0:
                break
            else:
                up_spots -= 1
                break
        while y+(down_spots+1)<15:
            #print "in second column while loop"
            if self.board.item((x,y+(down_spots+1))) == None:
                down_spots += 1
                if self.board.item((x-1,y+(down_spots))) != None or self.board.item((x+1,y+(down_spots))) != None:
                    down_spots -= 1
                    break
            elif down_spots == 0:
                break
            else:
                down_spots -= 1
                break
        self.players[0].open_spots[-1].append([up_spots,down_spots])

"""Brain Dump by Shruti (Need not read): Could possibly do multiple letters, return 
a list of words and then crosscheck it with the proposed board to avoid writing over 
the existing board. For cross-checking, add the chosen spot to a list with Nones and 
letters already on the board"""

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

    def update_score(self,word):
        word_list = [line.strip() for line in open("words.txt", 'r')]
        print word
        if word.lower() in word_list:
            for letter in word:
                self.score += self.model.points[letter]
        else:
            print 'not in word list'

class Artificial(object):
    def __init__(self,model,name):
        self.player = Player(model, name)

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
        self.placed_letters = []

    def count_tiles(self,model):
        return 7-len(self.letters_inhand)

    def pick_letters(self,model):
        for i in range(self.count_tiles(model)):
            letter = self.model.bag_contents.pickTile()
            self.letters_inhand.append(LetterTile(letter, "letter_tiles/" + letter + ".png", 37, 37, 20, 640))

    def define_coordinates(self, model):
        index = 0
        for item in self.letters_inhand:
            item.x = 160 + index*40
            item.y = 640
            index += 1

    def add_placed_tile(self,letter):
        self.placed_letters.append(letter)

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