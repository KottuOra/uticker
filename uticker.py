#!/usr/bin/env python
import logging
import config
import tickersources 
import threading
import time
from datetime import datetime as dt
from colorsys import hsv_to_rgb
from PIL import ImageFont
from scrollable import Scrollable
from unicornhatmini import UnicornHATMini
import os
dir = os.path.dirname(__file__)

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
tickercontent={}

#prepare the unicornhat for display
unicornhatmini = UnicornHATMini()


def update_content():
    global tickercontent
    logging.info('Updating content...')
    content = {}
    font = ImageFont.truetype(os.path.join(dir, config.general["font"]), 8) 
    shape = (17,7)
    if (config.weather["enabled"]):
        content["weather"] = Scrollable("weather",tickersources.get_weather(),tickersources.config.weather["color"],font,shape)  
    if (config.trends["enabled"]):
        content["twitter"] = Scrollable("twitter",tickersources.get_trends(),tickersources.config.trends["color"],font,shape)  
    if (config.exchange["enabled"]):
        content["exchange"] = Scrollable("exchange",tickersources.get_exchange(),tickersources.config.exchange["color"],font,shape)  
    if (config.news["enabled"]):
        content["news"] = Scrollable("news",tickersources.get_news(),tickersources.config.news["color"],font,shape)  
    tickercontent = content
    logging.debug("Content updated:" + "{0}".format(content))

def content_loop():
    logging.info('Content update loop started')
    while True:  
        time.sleep(config.general["data_refresh"])
        update_content()

def dim_brightness():
    global unicornhatmini
    if (config.general["night_mode"]):
        currenthour = dt.now().hour
        logging.info('Current Hour: %d ' , currenthour )
        if(  (currenthour > config.general["day_starts"]) and (currenthour < config.general["night_starts"]) ):
            unicornhatmini.set_brightness(config.general["brightness"])
            logging.debug('setting the daytime brigthness.')
        else:
            unicornhatmini.set_brightness(config.general["night_brightness"])
            logging.debug('setting the nighttime brigthness.')

def set_screen_pixels(image,offset_x, offset_y, color):
    global unicornhatmini
    display_width, display_height = unicornhatmini.get_shape()
    (r, g, b) = color

    for y in range(display_height):
        for x in range(display_width):
            if image.getpixel((x + offset_x, y+offset_y)) == 255:
                unicornhatmini.set_pixel(x, y, r, g, b)
            else:
                unicornhatmini.set_pixel(x, y, 0, 0, 0)

def main():
    global unicornhatmini
    global tickercontent
    logging.info("Starting ..:: uticker ::..")
    #get the initial content 
    logging.info("Getting the initial content to display")
    update_content()

    #kick-off the content update loop
    logging.info("Kicking off the content loop")
    content_thread = threading.Thread(target=content_loop, args=())
    content_thread.start()
    #content_thread.join()


    logging.debug("Initial Display setup")


    # Uncomment the below if your display is upside down
    #   (e.g. if you're using it in a Pimoroni Scroll Bot)
    unicornhatmini.set_rotation(config.general["rotate"])

    # Dial down the brightness
    dim_brightness()

    # Delay is the time (in seconds) between each pixel scrolled
    delay = config.general["delay"]    
    logging.info("initial set-up done")

    logging.info("Entering the main loop, for uticker.")
    while True:
        loop_start = time.time()
        display_width, display_height = unicornhatmini.get_shape()
        unicornhatmini.clear()
        #dim brightness check each loop 
        dim_brightness()
        color = (255,0,0)
        logging.debug("random color %s",color)
        
        for key  in tickercontent.keys():
            content = tickercontent[key]

            logging.debug('scroll content %s - with %d lines', content.category, len(content.lengths))
            #1. get the content and the imagebuffer 
            image = content.image
            color = content.color
            #2. get the content and start looping over lines 
            for i in range(len(content.lengths)):
                linelength = content.lengths[i] 
                #3. Lift content effect per each line, start with a lift
                #reset the x offset and start rolling the line up
                offset_x = 0
                offset_y = i*display_height*2 
                logging.debug('lifting y_offset %d ', offset_y)
                while offset_y <= i*display_height*2+display_height:
                    set_screen_pixels(image,offset_x,offset_y,color)
                    offset_y += 1
                    unicornhatmini.show()
                    time.sleep(delay)    
                #wait a bit longer after lifting the line for better visualisation 
                time.sleep(delay*10) 
                #4. Scroll the content until the length
                offset_x = 0
                offset_y = (2*i + 1 )*display_height
                logging.debug('scrolling x_offset %d and y_offset %d', offset_x, offset_y)
                while offset_x + display_width < linelength:
                    set_screen_pixels(image,offset_x,offset_y,color)
                    offset_x += 1
                    unicornhatmini.show()
                    time.sleep(delay)
        logging.info("Finished scrolling full content in %d seconds",  time.time()- loop_start)

if __name__ == "__main__":
    main()
