# Playing audio on a pi zero

## Setup
Add the following lines to the end of the config.txt file in the boot partition of the pi. This will reroute pwm outputs for audio on pins 18 and 13 (BCM) and map an audio device that alsa can use.

### Configure audio - redirect PWM output
dtoverlay=pwm-2chan,pin=18,func=2,pin2=13,func2=4
dtoverlay=audremap,enable_jack=on
