"""Waits for gpio input and plays sound via a subprocess"""
import os
import sys
import time

import RPi.GPIO as gpio

from sound import SoundPlayer
from inputoutput import SwitchPoller

# Setup so that the input is normally high and when it goes low is assumed to be activated.
BCM_PIN_IDX = 17
gpio.setmode(gpio.BCM)
gpio.setup(BCM_PIN_IDX, gpio.IN, pull_up_down=gpio.PUD_UP)

HERE_ABSDIR = sys.path[0]
WAV_LIBPATH = os.path.join(HERE_ABSDIR, 'wav')
SOUNDER_ABSPATH = os.path.join(WAV_LIBPATH, 'emergency.wav')
READY_ABSPATH = os.path.join(WAV_LIBPATH, 'ready.wav')

ALARM_SOUNDER = SoundPlayer(SOUNDER_ABSPATH)
SWITCHPOLLER = SwitchPoller(
    read_state=lambda: not gpio.input(BCM_PIN_IDX),
    callback=lambda state: ALARM_SOUNDER.play() if state else ALARM_SOUNDER.stop(),
)
SWITCHPOLLER.start()

print("Waiting for button press...")
SoundPlayer(READY_ABSPATH).play()
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("Quitting...")
        SWITCHPOLLER.stop()
        SWITCHPOLLER.join()
        break

gpio.cleanup()
