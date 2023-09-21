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

debug_loop=False

zones = {
    'greenhouse': 'yellow',
    'front': 'green',
    'frontside': 'blue',
    'unused_4': 'brown',
    'unused_5': 'red',
    }

colorpins = {
    'yellow': pins[0],
    'green': pins[1],
    'dead_relay': pins[2],
    'blue': pins[3],
    'brown': pins[4],
    'red': pins[5],
    'orange': pins[6],
}
print(colorpins)

def get_pin(s):
    if s in zones:
        return colorpins[zones[s]]
    if s in colorpins:
        return colorpins[s]
    return None

def help():
    print('usage: water.py <zone> <num_minutes> | stop')
    sys.exit(1)

def main():
    setup_logging()

    stop = False
    if len(sys.argv) == 2:
        if sys.argv[1] == 'stop':
            stop = True
        else:
            help()
    elif len(sys.argv) != 3:
        help()

    if stop:
        print('stopping all zones')
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, GPIO.HIGH) # should be default, but add here to be safe
        sys.exit(0)

    zone = sys.argv[1]
    num_minutes = int(sys.argv[2])
    duration_seconds = num_minutes*60

    pin = get_pin(zone)
    if pin is None:
        print(f'invalid zone {zone}')
        sys.exit(1)

    logging.info(f'water scheduler started; {zone} (pin {pin}) for {num_minutes}')
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    for p in pins:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.HIGH) # should be default, but add here to be safe
    
    try:
        while 1:
            logging.info(f'turning {zone} (pin {pin}) on')
            GPIO.output(pin, GPIO.LOW) # turn water on
            time.sleep( duration_seconds )
            logging.info(f'turning {zone} (pin {pin}) off')
            GPIO.output(pin, GPIO.HIGH) # turn water off
            if debug_loop:
                time.sleep( duration_seconds )
                continue
            break
    except BaseException as e:
        logging.info(f'unexpected {e=}')
        raise
    finally:
        logging.info(f'turning {zone} off')
        GPIO.output(pin, GPIO.HIGH) # turn water off just in case

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
