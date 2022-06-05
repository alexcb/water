# External module imports
import RPi.GPIO as GPIO
import time

# The GPIO.BCM option means that you are referring to the pins by the "Broadcom SOC channel" number,
# these are the numbers after "GPIO" in the green rectangles around the outside of the below diagrams:

# ordered from relay 1 to 8
pins = [25, 10, 24, 23, 22, 27, 17, 18]

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH) # should be default, but add here to be safe

i = 0
try:
    while 1:
        pin = pins[i]
        GPIO.output(pin, GPIO.LOW)
        time.sleep( 0.5 )
        GPIO.output(pin, GPIO.HIGH)
        time.sleep( 0.1 )
        i = (i+1) % len(pins)
finally:
    print('exit')
    GPIO.cleanup()
