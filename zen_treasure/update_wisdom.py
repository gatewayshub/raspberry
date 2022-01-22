#!/usr/bin/python
#args: 0 - 9 zen wisdom with specified index... 10 random wisdom will be selected

import sys
import os
import textwrap
import feedparser
import random

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import PIL

logging.basicConfig(level=logging.DEBUG)

RANDOM=10

def get_zen(x):
    #Get wisdom from feed by id... if id = 10 get random wisdom
    d = feedparser.parse('https://www.zen-guide.de/zen/rss/')
    if x == RANDOM:
        length = len(d['entries'])
        x = random.randint(1,length-1)
    return d.entries[x].summary


try:
    try:
        arg = sys.argv[1]
        arg = int(arg)
        if arg > 10 or arg < 0:
            arg = 0
    except:
        arg = 0

    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    # Drawing on the image
    font_ps =  ImageFont.truetype('DejaVuSansMono.ttf', 12)
    
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    #blurb = get_zen(RANDOM)
    blurb = get_zen(arg)
   

    blurb = textwrap.wrap(blurb, 35)

    offset = 4 - int(len(blurb)/2)
    if offset < 0:
        offset = 0

    for x, line in enumerate(blurb):
                #line = line.encode('UTF-8').decode('LATIN-1')
                draw.text((0, 2 + (x * 13) + (offset * 13)), text=line, font=font_ps, fill=0)

    image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM).transpose(PIL.Image.FLIP_LEFT_RIGHT)
    epd.display(epd.getbuffer(image))

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
