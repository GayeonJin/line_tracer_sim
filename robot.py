#!/usr/bin/python

import sys
import math
import pygame
import random

from gresource import *

DEFAULT_ANGLE = 90

class robot :
    def __init__(self, x, y) :
        self.object = pygame.image.load('image/mouse.png')
        self.width = self.object.get_width()
        self.height = self.object.get_height()

        # angle unit is degree
        self.angle = DEFAULT_ANGLE

        self.set_position(x, y)

    def set_position(self, x, y) : 
        # (x, y) is center position
        self.x = x
        self.y = y
 
    def move(self, velocity) :
        del_x = velocity * math.cos(math.radians(self.angle))

        # left, top is (0, 0) -> need minus
        del_y = -velocity * math.sin(math.radians(self.angle))
        self.x += del_x
        self.y += del_y

    def rotate(self, del_theta) :
        self.angle += del_theta
        if self.angle >= 360 :
            self.angle = 0
        elif self.angle < 0 :
            self.angle = 360

    def draw(self) :
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        rect.centerx = self.x
        rect.centery = self.y

        offset_center_to_pivot = pygame.math.Vector2(rect.x, rect.y) - (self.x, self.y)
        #rotated_offset = offset_center_to_pivot.rotate(self.angle - DEFAULT_ANGLE)

        rotate_img = pygame.transform.rotate(self.object, self.angle - DEFAULT_ANGLE)
        rotated_image_rect = rotate_img.get_rect(center = (self.x, self.y))
       
        gctrl.surface.blit(rotate_img, rotated_image_rect)
 
if __name__ == '__main__' :
    print('robot')