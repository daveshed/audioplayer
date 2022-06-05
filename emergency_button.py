#! /usr/bin/python3
import os
import sys
import time
import subprocess

import RPi.GPIO as gpio
# setup so that the input is normally high and when it goes low, the event handler
# will be called....
BCM_PIN_IDX = 17
HERE_ABSDIR = sys.path[0]
AUDIO_FILENAME = 'emergency.wav'
AUDIO_ABSPATH = os.path.join(HERE_ABSDIR, AUDIO_FILENAME)
gpio.setmode(gpio.BCM)
gpio.setup(BCM_PIN_IDX, gpio.IN, pull_up_down=gpio.PUD_UP)

def event_handler(channel):
    print(f"handling button press '{gpio.input(BCM_PIN_IDX)}'")
    if gpio.input(BCM_PIN_IDX):
        return
    subprocess.run(['aplay', AUDIO_ABSPATH])

gpio.add_event_detect(BCM_PIN_IDX, gpio.FALLING, callback=event_handler, bouncetime=2000)

print("Waiting for button press...")
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("Quitting...")
        break

gpio.cleanup()
