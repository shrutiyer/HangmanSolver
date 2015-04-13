"""
Shruti(4/13/15): I think the game is working fine. I added a list of english  and it checks 
if the word is legal or not. I didn't spend a lot of time finding bugs. But, 
the game looks almost complete
"""
import pygame
from pygame.locals import *
import random
import math
import time
import numpy as np
import copy

import Model
import View
import Control

# if __name__ == '__main__':
pygame.init()

size = (600,700)
screen = pygame.display.set_mode(size)

model = Model.Model()
view = View.PyGameWindowView(model,screen)

controller = Control.PyGameController(model)

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
