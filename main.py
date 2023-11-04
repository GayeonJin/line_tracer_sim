#!/usr/bin/python

import os
import sys
import csv

import pygame
import random
from time import sleep

from gresource import *
from robot import *

from field import *
from cursor import *

TITLE_STR = "Line Tracer"

INFO_HEIGHT = 40
INFO_OFFSET = 10
INFO_FONT = 14

def draw_info() :
    font = pygame.font.SysFont('Verdana', INFO_FONT)
    info = font.render('F1/F2 : Load/Save field file    space : toggle', True, COLOR_BLACK)

    pygame.draw.rect(gctrl.surface, COLOR_PURPLE, (0, gctrl.height - INFO_HEIGHT, gctrl.width, INFO_HEIGHT))
    gctrl.surface.blit(info, (INFO_OFFSET * 2, gctrl.height - 2 * INFO_FONT - INFO_OFFSET))

def draw_robot_info() :
    global robot_object
    
    font = pygame.font.SysFont('Verdana', 20)
    info = font.render('pos : %d, %d'%(robot_object.x, robot_object.y), True, COLOR_BLACK)
    gctrl.surface.blit(info, (10, 10))
    info = font.render('angle : %d deg'%(robot_object.angle), True, COLOR_BLACK)
    gctrl.surface.blit(info, (10, 30))    

def draw_message(str) :
    font = pygame.font.Font('freesansbold.ttf', 40)
    text_suf = font.render(str, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))

    gctrl.surface.blit(text_suf, text_rect)
    pygame.display.update()
    sleep(2)

def terminate() :
    pygame.quit()
    sys.exit()

def edit_field() :
    global clock
    global field_map

    cursor = cursor_object(field_map)
    cursor.x = 0
    cursor.y = 0

    direction = 0
    
    pre_x = 0
    pre_y = 0
    mouse_drag = False

    pixel_toggel = 0
    edit_exit = False
    while not edit_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                edit_exit = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP:
                    direction = CURSOR_MOVE_UP
                elif event.key == pygame.K_DOWN :
                    direction = CURSOR_MOVE_DOWN
                elif event.key == pygame.K_LEFT :
                    direction = CURSOR_MOVE_LEFT
                elif event.key == pygame.K_RIGHT :
                    direction = CURSOR_MOVE_RIGHT
                elif event.key == pygame.K_SPACE :
                    pixel_toggel = 1
                elif event.key == pygame.K_F1 :               
                    field_map.load_file()
                elif event.key == pygame.K_F2 :
                    field_map.save_file()
                elif event.key == pygame.K_x :
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN :
                l_button, wheel, r_button = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                x, y = field_map.get_pos(mouse_pos)
                if x != None or y != None :
                    mouse_drag = True
                    cursor.set_pos(x, y)
                    if l_button :
                        field_map.set(cursor.x, cursor.y)
                    elif r_button :
                        field_map.clear(cursor.x, cursor.y)
                    pre_x = x
                    pre_y = y                    
            elif event.type == pygame.MOUSEMOTION :
                if mouse_drag == True :
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = field_map.get_pos(mouse_pos)
                    if x != None or y != None :
                        if pre_x != x or pre_y != y :
                            cursor.set_pos(x, y)
                            if l_button :
                                field_map.set(cursor.x, cursor.y) 
                            elif r_button :
                                field_map.clear(cursor.x, cursor.y)                           
                            pre_x = x
                            pre_y = y
            elif event.type == pygame.MOUSEBUTTONUP :
                mouse_drag = False
                mouse_pos = pygame.mouse.get_pos()
                x, y = field_map.get_pos(mouse_pos)
                if x != None or y != None :
                    if pre_x != x or pre_y != y :
                        cursor.set_pos(x, y)
                        if l_button :
                            field_map.set(cursor.x, cursor.y)
                        elif r_button :
                            field_map.clear(cursor.x, cursor.y)                          
                        pre_x = x
                        pre_y = y

        # Move cursor
        if direction != 0 :
            cursor.move(direction)
            direction = 0

        # Change pixel
        if pixel_toggel != 0 :
            field_map.toggle(cursor.x, cursor.y)
            pixel_toggel = 0
            
        # Clear surface
        gctrl.surface.fill(COLOR_WHITE)

        # Draw field_map
        field_map.draw()

        # Draw cursor
        cursor.draw_rect(COLOR_BLACK, 1)

        # Draw Info
        draw_info()

        pygame.display.update()
        clock.tick(60)

def test_robot() :
    global field_map, robot_object

    keys = {}
    keys[pygame.K_RIGHT] = False
    keys[pygame.K_LEFT] = False

    vel = 0
    test_exit = False
    while not test_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                test_exit = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP :
                    if vel <= 5 :
                        vel += 1
                elif event.key == pygame.K_DOWN :
                    if vel >= 0 :
                        vel -= 1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT :
                    keys[event.key] = False
                elif event.key == pygame.K_x :
                    return
                
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT :
                    keys[event.key] = True 

        # Clear surface
        gctrl.surface.fill(COLOR_WHITE)

        # Control robot
        if keys[pygame.K_RIGHT] :
            robot_object.rotate(-1)
        elif keys[pygame.K_LEFT] :
            robot_object.rotate(1)

        robot_object.move(vel)

        # Draw robot
        robot_object.draw()
        draw_robot_info()

        pygame.display.update()
        clock.tick(60)

def start_line_tracer() :
    # Clear surface
    gctrl.surface.fill(COLOR_WHITE)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text_suf = font.render(TITLE_STR, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))
    gctrl.surface.blit(text_suf, text_rect)

    help_str = ['e : edit field',
                't : test robot',
                'x : exit']

    font1 = pygame.font.SysFont(None, 25)
    for i, help in enumerate(help_str) :
        text_suf1 = font1.render(help, True, COLOR_BLUE)
        text_rect1 = text_suf1.get_rect()
        text_rect1.top = text_rect.bottom + 50 + i * 25
        text_rect1.centerx = gctrl.width / 2
        gctrl.surface.blit(text_suf1, text_rect1)

    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_e :
                    return 'edit'
                elif event.key == pygame.K_t :
                    return 'test'
                elif event.key == pygame.K_x :
                    terminate()

        pygame.display.update()
        clock.tick(60)    
       
def init_line_tracer() :
    global clock
    global field_map, robot_object

    pygame.init()
    clock = pygame.time.Clock()

    # field_map
    field_map = field(MAX_ROWS, MAX_COLS)
    (pad_width, pad_height) = field_map.get_padsize()

    # robot
    robot_object = robot(pad_width / 2, pad_height / 2)

    pad_height += INFO_HEIGHT
    
    gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
    pygame.display.set_caption(TITLE_STR)

if __name__ == '__main__' :
    init_line_tracer()
    while True :
        mode = start_line_tracer()
        if mode == 'edit' :
            edit_field()
        elif mode == 'test' :
            test_robot()

