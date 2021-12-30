#!/usr/bin/python

from sense_hat import SenseHat
import time, datetime, random


#init vars
sense = SenseHat()
sense.clear()

run_game = True

x_pixel = 0
y_pixel = 0
pixel_catched = False
victory_counter = 0
start_time = time.time()
time_end = start_time + 20

#Init first target
x_target = random.randrange(7)
y_target = random.randrange(7)
sense.set_pixel(x_target,y_target,(255,0,0))


while run_game:
    if pixel_catched == False:
        #if pixel isn´t catched get accel values and go on with movement
        x,y,z = sense.get_accelerometer_raw().values()
        sense.set_pixel(x_pixel,y_pixel,(0,0,0))
        x_pixel = int(x*4+4)
        y_pixel = int(y*4+4)
        if x_pixel > 7:
            x_pixel = 7
        if y_pixel > 7:
            y_pixel = 7
        if x_pixel < 0:
            x_pixel = 0
        if y_pixel < 0:
            y_pixel = 0
        #sense.clear()
        sense.set_pixel(x_pixel,y_pixel, (0, 255, 0))
        #print("%s, %s, %s" %(x,y,z))
        #time.sleep(0.2)
    else:
        #if target is catched init new one and reset pixel_catched afterwards
        x_target = random.randrange(8)
        y_target = random.randrange(8)
        sense.set_pixel(x_target,y_target,(255,0,0))
        pixel_catched = False
    
    if x_pixel == x_target and y_pixel == y_target:
        #if target is catched set pixel_catched true to get new target and count up victory_counter - also check if game_time exceeded
        print("Catched")
        pixel_catched = True
        victory_counter += 1
        if time_end <= time.time():
            run_game = False
            
#sense.set_rotation(180)
sense.show_message(str(victory_counter))
sense.show_message("Points")
