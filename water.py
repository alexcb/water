# External module imports
import RPi.GPIO as GPIO
import time

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

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH) # should be default, but add here to be safe

pin = zones['greenhouse']
try:
    while 1:
        GPIO.output(pin, GPIO.LOW) # turn water on
        time.sleep( 10 )
        GPIO.output(pin, GPIO.HIGH) # turn water off
        time.sleep( 50 )
finally:
    print('exit')
    GPIO.cleanup()
