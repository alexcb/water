#!/usr/bin/env python3

# External module imports
import RPi.GPIO as GPIO
import time
import datetime
import logging
import sys

# The GPIO.BCM option means that you are referring to the pins by the "Broadcom SOC channel" number,
# these are the numbers after "GPIO" in the green rectangles around the outside of the below diagrams:

# ordered from relay 1 to 8
pins = [25, 10, 24, 23, 22, 27, 17, 18]

zones = {
    'greenhouse': pins[0], # yellow
    'unused_1': pins[1], # green
    'unused_2': pins[2], # orange
    'unused_3': pins[3], # blue
    'unused_4': pins[4], # brown
    'unused_5': pins[5], # red
    }

def main():
    setup_logging()
    logging.info(f'water scheduler started')
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH) # should be default, but add here to be safe
    
    zone = 'greenhouse'
    pin = zones['greenhouse']
    try:
        while 1:
            now = datetime.datetime.now()
            logging.info(f'turning {zone} on')
            GPIO.output(pin, GPIO.LOW) # turn water on
            time.sleep( 10*60 )
            logging.info(f'turning {zone} off')
            GPIO.output(pin, GPIO.HIGH) # turn water off
            #time.sleep( 50 )
            break
    except BaseException as e:
        logging.info(f'unexpected {e=}')
        raise
    finally:
        GPIO.cleanup()
        logging.info(f'water scheduler exiting')

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.DEBUG)
    stderr_handler.setFormatter(formatter)
    
    file_handler = logging.FileHandler('/root/water.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(stderr_handler)

if __name__ == '__main__':
    main()
