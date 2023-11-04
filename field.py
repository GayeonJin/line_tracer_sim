#!/usr/bin/python

import sys
import csv

import pygame

from gresource import *
from robot import *

MAX_ROWS = 60
MAX_COLS = 120

MAP_XOFFSET = 10
MAP_YOFFSET = 30

MAP_WIDTH = 8 * MAX_COLS
MAP_HEIGHT = 8 * MAX_ROWS

class field :
    def __init__(self, rows, cols) :
        self.map = []

        self.rows = rows
        self.cols = cols
        
        for x in range(self.cols) :
            self.map.append([])
            for y in range(self.rows) :
                self.map[x].append(0)

        self.x_offset = MAP_XOFFSET
        self.y_offset = MAP_YOFFSET

        self.obj_width = int(MAP_WIDTH / self.cols)
        self.obj_height = int(MAP_HEIGHT / self.rows)

    def get_size(self) :
        return self.rows, self.cols

    def set_rect(self, rect) :
        self.x_offset = rect.x
        self.y_offset = rect.y
        self.obj_width = rect.width / self.cols
        self.obj_height = rect.height /self.rows
       
    def get_padsize(self) :
        pad_width = 2 * self.x_offset + self.cols * self.obj_width 
        pad_height = 2 * self.y_offset + self.rows * self.obj_height
        return (pad_width, pad_height) 

    def get_bitmap(self) :
        return self.map

    def get_map_rect(self, x, y) :
        map_rect = pygame.Rect(self.x_offset, self.y_offset, self.obj_width , self.obj_height)

        # map[0][0] is left and bottom
        map_rect.x += x * self.obj_width 
        map_rect.y += y * self.obj_height
        return map_rect        

    def get_pos(self, screen_xy) :
        # map[0][0] is left and top
        for y in range(self.rows) :
            for x in range(self.cols) :
                map_rect = self.get_map_rect(x, y)
                if screen_xy[0] > map_rect.left and screen_xy[0] < map_rect.right :
                    if screen_xy[1] > map_rect.top and screen_xy[1] < map_rect.bottom :      
                        return (x, y)
                    
        return (None, None)

    def toggle(self, x, y) :
        if self.map[x][y] == 1 :
            self.map[x][y] = 0
        else :
            self.map[x][y] = 1

    def set(self, x, y) :
        self.map[x][y] = 1

    def clear(self, x, y) :
        self.map[x][y] = 0     

    def draw(self, real_size = False) :
        map_rect = pygame.Rect(self.x_offset, self.y_offset, self.obj_width, self.obj_height)

        # map[0][0] is left and top
        for y in range(self.rows) :
            for x in range(self.cols) :
                if real_size == False :
                    pygame.draw.rect(gctrl.surface, COLOR_RED, map_rect, 1, 1)
                if self.map[x][y] == 1 :
                    pygame.draw.rect(gctrl.surface, COLOR_BLACK, map_rect)

                map_rect.x += self.obj_width
            map_rect.y += self.obj_height
            map_rect.x = self.x_offset

    def load_file(self, filename = 'default_field.csv') :
        print("load field : " + filename)

        file = open(filename, 'r')
        rows = csv.reader(file)

        for y, row_data in enumerate(rows) :
            for x, value in enumerate(row_data) :
                self.map[x][y] = int(value)

    def save_file(self, filename = 'default_field.csv') :
        print("save field : " + filename)

        with open(filename, 'w') as file:
            #for header in header:
            #    file.write(str(header)+', ')
            #file.write('n')
            for y in range(self.rows) :
                for x in range(self.cols - 1):                    
                    file.write(str(self.map[x][y])+', ')
                file.write(str(self.map[x + 1][y])+'\n')

if __name__ == '__main__' :
    print('field class')
