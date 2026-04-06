from machine import Pin
from utime import sleep

button_happy = Pin(2, Pin.IN, Pin.PULL_UP)
button_meh = Pin(1, Pin.IN, Pin.PULL_UP)
button_sad = Pin(0, Pin.IN, Pin.PULL_UP)

happy = 0
meh = 0
sad = 0

happy_pressed = False
meh_pressed = False
sad_pressed = False
    
while True:

    if button_happy.value() == 0 and not happy_pressed:
        happy_pressed = True
        happy += 1
    elif button_happy.value() == 1:
        happy_pressed = False
    
    if button_meh.value() == 0 and not meh_pressed:
        meh_pressed = True
        meh += 1
    elif button_meh.value() == 1:
        meh_pressed = False
    
    if button_sad.value() == 0 and not sad_pressed:
        sad_pressed = True
        sad += 1
    elif button_sad.value() == 1:
        sad_pressed = False
        
    print(f"Happy: {happy}")
    print(f"meh: {meh}")
    print(f"sad: {sad}")
    sleep(.1)