import pygame
from pygame.locals import *
import random
import math
import time
import numpy as np
import copy
from tree import Tree,Node
import aitree
import View
import Control
import pickle

import Model

# if __name__ == '__main__':
pygame.init()

size = (600,700)
screen = pygame.display.set_mode(size)

model = Model.Model()
view = View.PyGameWindowView(model,screen)
controller = Control.PyGameController(model,view)

print 'Welcome to Scrabble Solver! You are player 1.'
print 'Try to beat our two AIs, Richard and Nixon.'
print """Instructions:
To select a letter, left click. 
To place the letter, right click.
To finish your move, press the space bar. 
If you can't find a move to make then press the space bar.
When it's an AI's turn you can left click to make them play their move."""
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
