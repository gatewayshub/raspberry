#!/usr/bin/env python
# 
# Library for ps_eval_board 
# Buttons on GPIO 26, 19, 13, 6
# Leds on GPIO 4, 17, 27, 22
# methods:
# button1_pressed() -> returns 0 or 1 ... checks button1
# button2_pressed() -> returns 0 or 1 ... checks button2 
# button3_pressed() -> returns 0 or 1 ... checks button3
# button4_pressed() -> returns 0 or 1 ... checks button4
# get_key_pressed() -> returns 0 or 1 ... checks all buttons at once
# get_which_key_pressed() -> returns 1, 2, 3, 4 ... indicates which button is pressed (0 for none)
# set_led(x) -> x is 1 to 4 to turn on one specific led
# set_led_bits(x) -> 4 bits of x will be used to display binary number
# set_display_text(text) -> text will be split into lines of 20 characters
# set_display_lines(lines) -> lines array will be displayed 
# get_device() -> returns oled device 

import sys
import time
from luma.core.virtual import viewport
from luma.core.render import canvas
from luma.core import cmdline, error
from PIL import ImageFont
import textwrap
import RPi.GPIO as GPIO


class EVAL_BOARD:
    def __init__(self):
        self.BUTTON_array = [6,13,19,26]
        self.LED_array = [4,17,27,22]
        
        #Select Font
        self.oled_font = ImageFont.truetype('DejaVuSansMono.ttf', 10)

        #Setup GPIO
        GPIO.setmode(GPIO.BCM)

        #Initialize leds and buttons
        GPIO.setup(self.LED_array[0], GPIO.OUT)
        GPIO.setup(self.LED_array[1], GPIO.OUT)
        GPIO.setup(self.LED_array[2], GPIO.OUT)
        GPIO.setup(self.LED_array[3], GPIO.OUT)
        GPIO.setup(self.BUTTON_array[0], GPIO.IN)
        GPIO.setup(self.BUTTON_array[1], GPIO.IN)
        GPIO.setup(self.BUTTON_array[2], GPIO.IN)
        GPIO.setup(self.BUTTON_array[3], GPIO.IN)
        
        #Initialize display args
        self.parser = cmdline.create_parser(description='Default args')
        self.args = self.parser.parse_args()

        # create device
        try:
            self.device = cmdline.create_device(self.args)

        except error.Error as e:
            self.parser.error(e)

        self.virtual = viewport(self.device, width=self.device.width, height=768)


    def button1_pressed(self):
        return GPIO.input(self.BUTTON_array[0])

    def button2_pressed(self):
        return GPIO.input(self.BUTTON_array[1])

    def button3_pressed(self):
        return GPIO.input(self.BUTTON_array[2])

    def button4_pressed(self):
        return GPIO.input(self.BUTTON_array[3])


    def get_key_pressed(self):
        if self.button1_pressed() == 1 or self.button2_pressed() == 1 or self.button3_pressed() == 1 or self.button4_pressed() == 1:
            return 1
        else:
            return 0
        
    def get_which_key_pressed(self):
        if self.button1_pressed():
            return 1
        elif self.button2_pressed():
            return 2
        elif self.button3_pressed():
            return 3
        elif self.button4_pressed():
            return 4
        else:
            return 0
        
    def set_led(self,led):
        if led == 1:
            self.set_led_bits(0b0001)
        if led == 2:
            self.set_led_bits(0b0010)
        if led == 3:
            self.set_led_bits(0b0100)
        if led == 4:
            self.set_led_bits(0b1000)

    def set_led_bits(self,led):
        if led & 0b1000:
            GPIO.output(self.LED_array[0], GPIO.HIGH)
        else:
            GPIO.output(self.LED_array[0], GPIO.LOW)
        if led & 0b0100:
            GPIO.output(self.LED_array[1], GPIO.HIGH)
        else:
            GPIO.output(self.LED_array[1], GPIO.LOW)
        if led & 0b0010:
            GPIO.output(self.LED_array[2], GPIO.HIGH)
        else:
            GPIO.output(self.LED_array[2], GPIO.LOW)
        if led & 0b0001:
            GPIO.output(self.LED_array[3], GPIO.HIGH)
        else:
            GPIO.output(self.LED_array[3], GPIO.LOW)

    def set_display_text(self,text):
        #Set new display text
        text = textwrap.wrap(text, 20)

        self.virtual.set_position((0,0))

        for _ in range(2):
            with canvas(self.virtual) as draw:
                for x, line in enumerate(text):
                    #line = line.encode('UTF-8').decode('LATIN-1')
                    draw.text((0, 2 + (x * 12)), text=line, font=self.oled_font, fill="white")
    
    def set_display_lines(self,lines):
        
        self.virtual.set_position((0,0))
        
        with canvas(self.virtual) as draw:
            for x, line in enumerate(lines):
                draw.text((0, 2 + (x * 12)), text=line, font=self.oled_font, fill="white")

    def get_device(self):
        return self.device
                

def main():
    global board
    a = 0b1000

    board.set_display_lines(["1.Zeile", "2.Zeile", "3.Zeile", "4.Zeile", "5.Zeile"])
    while True:
        #board.set_display_lines(["1.Zeile", "2.Zeile", "3.Zeile", "4.Zeile", "5.Zeile"])
        #a = 0b1000
        while a != 0b0001:
            a = a >> 1
            board.set_led_bits(a)
            time.sleep(0.1)
            button = board.get_which_key_pressed()
            if button != 0:
                board.set_display_text("Button" + str(button) + " pressed!!!")
            
        while a != 0b1000:
            a = a << 1
            board.set_led_bits(a)
            time.sleep(0.1)
            button = board.get_which_key_pressed()
            if button != 0:
                board.set_display_text("Button" + str(button) + " pressed!!!")
            

if __name__ == "__main__":
    try:
        board = EVAL_BOARD()
        main()

    except KeyboardInterrupt:
        pass
