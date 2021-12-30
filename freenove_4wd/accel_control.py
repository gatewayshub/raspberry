#!/usr/bin/python

from sense_hat import SenseHat
import time, datetime
import socket

sense = SenseHat()

TCP_IP = '192.168.5.232'
TCP_PORT = 5000
BUFFER_SIZE = 1024
MESSAGE = "CMD_MOTOR#0#0#0#0\n"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode())

run_loop = True

servo_h = 90 #id0
servo_v = 90 #id1


while run_loop:
    x,y,z = sense.get_accelerometer_raw().values()
 
    x = round(x,2)
    y = round(y,2)
    z = round(z,2)
    
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
     
    a = 0
    a = x
    x = y
    y = -a
  
  
    sense.clear()
    sense.set_pixel(x_pixel,y_pixel, (0, 255, 0))
    
    threshold = 0.2
    
    if x > -threshold and x < threshold:
        x = 0
    if y > -threshold+0.2 and y < threshold+0.2:
        y = 0

    MESSAGE = "CMD_MOTOR#" + str((int(x*-1500)+int(y*-1500))*2) + "#" + str((int(x*-1500)+int(y*-1500))*2) + "#" + str((int(x*-1500)+int(y*1500))*2) + "#" + str((int(x*-1500)+int(y*1500))*2) + "\n"
    #MESSAGE = "CMD_MOTOR#" + str((int(x*-1500)+int(y*-1500))*2) + "#" + str(int(y*-1500)*2) + "#" + str((int(x*-1500)+int(y*1500))*2) + "#" + str(int(y*1500)*2) + "\n"

    s.send(MESSAGE.encode())
    
    print("%s, %s, %s" %(x,y,z))
    time.sleep(0.2)
    
    for event in sense.stick.get_events():
        print(event.direction, event.action)
        if event.direction == "middle":
            print("Aborting")
            run_loop = False
        else:
            if event.direction == "up" and (event.action == "pressed" or event.action == "held"):
                servo_v += 10
   
            
            if event.direction == "down" and (event.action == "pressed" or event.action == "held"):
                servo_v -= 10
            if event.direction == "left" and (event.action == "pressed" or event.action == "held"):
                servo_h -= 10
            if event.direction == "right" and (event.action == "pressed" or event.action == "held"):
                servo_h += 10
            if servo_v > 180:
                servo_v = 180
            if servo_v < 80:
                servo_v = 80
            if servo_h > 180:
                servo_h = 180
            if servo_h < 0:
                servo_h = 0
            MESSAGE = "CMD_SERVO#1#" + str(servo_v) + "\n"
            s.send(MESSAGE.encode())
            MESSAGE = "CMD_SERVO#0#" + str(servo_h) + "\n"
            s.send(MESSAGE.encode())
     

MESSAGE = "CMD_MOTOR#0#0#0#0\n"
s.send(MESSAGE.encode())
MESSAGE = "CMD_SERVO#0#90\n"
s.send(MESSAGE.encode())
MESSAGE = "CMD_SERVO#1#90\n"
s.send(MESSAGE.encode())
s.close()
