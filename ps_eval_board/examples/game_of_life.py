#!/usr/bin/env python

"""
Conway's game of life

Some extras for ps_eval_board...
Use 4 buttons to start with different initial population [0.9,0.4,0.23,0.15]
Indicate cycles with leds [0,100,200,300]
"""

import time
import sys
from random import randint
from luma.core.render import canvas
sys.path.append('../lib')
from ps_eval_board import *
import RPi.GPIO as GPIO


def neighbors(cell):
    x, y = cell
    yield x - 1, y - 1
    yield x, y - 1
    yield x + 1, y - 1
    yield x - 1, y
    yield x + 1, y
    yield x - 1, y + 1
    yield x, y + 1
    yield x + 1, y + 1


def apply_iteration(board):
    new_board = set([])
    candidates = board.union(set(n for cell in board for n in neighbors(cell)))
    for cell in candidates:
        #count = sum((n in board) for n in neighbors(cell))
        count = sum((n in board) for n in neighbors(cell))
        if count == 3 or (count == 2 and cell in board):
            new_board.add(cell)
    return new_board

def set_led(i):
    global eval_board

    if i > 0:
        eval_board.set_led_bits(0b1000)
    if i > 100:
        eval_board.set_led_bits(0b1100)
    if i > 200:
        eval_board.set_led_bits(0b1110)
    if i > 300:
        eval_board.set_led_bits(0b1111) 

def main():
    scale = 2
    cols = device.width // scale
    rows = device.height // scale
    population_factor = 0.5

    while True:
        set_led(400)
        initial_population = int(cols * rows * population_factor)
        board = set((randint(0, cols), randint(0, rows)) for _ in range(initial_population))
        set_led(0) 
        for i in range(400):
            key_pressed = eval_board.get_which_key_pressed()
            if key_pressed != 0:
                 population_factor = 1 / key_pressed - 0.1
                 break
                
            with canvas(device) as draw:
                for x, y in board:
                    left = x * scale 
                    top = y * scale
                    if scale == 1:
                        draw.point((left, top), fill="white")
                    else:
                        right = left + scale
                        bottom = top + scale
                        draw.rectangle((left, top, right, bottom), fill="white", outline="black")

            board = apply_iteration(board)
            set_led(i)


if __name__ == "__main__":
    try:
        eval_board = EVAL_BOARD()
        device = eval_board.get_device()
        

        set_led(400)
        main()
    except KeyboardInterrupt:
        pass
