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
import os
import scrollphathd

dir = os.path.dirname(__file__)

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
tickercontent={}

#prepare the unicornhat for display
#scrollphathd = scrollphathd()


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
    if (config.general["night_mode"]):
        currenthour = dt.now().hour
        logging.info('Current Hour: %d ' , currenthour )
        if(  (currenthour > config.general["day_starts"]) and (currenthour < config.general["night_starts"]) ):
            scrollphathd.set_brightness(config.general["brightness"])
            logging.debug('setting the daytime brigthness.')
        else:
            scrollphathd.set_brightness(config.general["night_brightness"])
            logging.debug('setting the nighttime brigthness.')

def set_screen_pixels(image,offset_x, offset_y, color):
    display_width, display_height = scrollphathd.get_shape()
    (r, g, b) = color

    for y in range(display_height):
        for x in range(display_width):
            if image.getpixel((x + offset_x, y+offset_y)) == 255:
                scrollphathd.set_pixel(x, y, r, g, b)
            else:
                scrollphathd.set_pixel(x, y, 0, 0, 0)

def main():
    
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
    scrollphathd.rotate(degrees=config.general["rotate"])

    # Dial down the brightness
    dim_brightness()
    rewind = False


    # Delay is the time (in seconds) between each pixel scrolled
    delay = config.general["delay"]    
    logging.info("initial set-up done")

    logging.info("Entering the main loop, for uticker.")
    while True:
        loop_start = time.time()
        scrollphathd.clear()
        #dim brightness check each loop 
        dim_brightness()
        line_height = scrollphathd.DISPLAY_HEIGHT + 2

        
        for key  in tickercontent.keys():
            scrollphathd.clear()
            scrollable = tickercontent[key]
            lines = ["   "] # put an empty line for vertical lift effect
            lines += scrollable.getTickerLines()
            logging.debug('scroll content %s - with %d lines', scrollable.category, len(lines))
            #1. prepare the text buffer 
            lengths = [0] * len(lines)
            # Store the left offset for each subsequent line (starts at the end of the last line)
            offset_left = 0            
            for line, text in enumerate(lines):
                lengths[line] = scrollphathd.write_string(text, x=offset_left, y=line_height * line)
                offset_left += lengths[line]
            # This adds a little bit of horizontal/vertical padding into the buffer at
            # the very bottom right of the last line to keep things wrapping nicely.
            scrollphathd.set_pixel(offset_left - 1, (len(lines) * line_height) - 1, 0)
            # Reset the animation
            scrollphathd.scroll_to(0, 0)
            scrollphathd.show()
            # Keep track of the X and Y position for the rewind effect
            pos_x = 0
            pos_y = 0
            for current_line, line_length in enumerate(lengths):
                # Delay a slightly longer time at the start of each line
                time.sleep(delay * 10)

                # Scroll to the end of the current line
                for y in range(line_length):
                    scrollphathd.scroll(1, 0)
                    pos_x += 1
                    time.sleep(delay)
                    scrollphathd.show()
                if not current_line == len(lines) - 1:
                    for x in range(line_height):
                        scrollphathd.scroll(0, 1)
                        pos_y += 1
                        scrollphathd.show()
                        time.sleep(delay)

        logging.info("Finished scrolling full content in %d seconds",  time.time()- loop_start)

if __name__ == "__main__":
    main()
