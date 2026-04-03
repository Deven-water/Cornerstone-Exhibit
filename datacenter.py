from machine import Pin, PWM
from utime import sleep
import machine, neopixel
from machine import ADC
import math
#import random

da = neopixel.NeoPixel(machine.Pin(13), 19)
en1 = neopixel.NeoPixel(machine.Pin(0), 29)
en2 = neopixel.NeoPixel(machine.Pin(1), 29)

recieve = Pin(15, Pin.IN)

data_lvl = neopixel.NeoPixel(machine.Pin(14), 10)

def change_green(RGB, length):
    for i in range(length):
        RGB[i] = (0, 125, 0)
        RGB.write()

def change_red(RGB, length):
    for i in range(length):
        RGB[i] = (125, 0, 0)
        RGB.write()

def change_white(RGB, length):
    for i in range(length):
        RGB[i] = (125, 125, 125)
        RGB.write()

def turn_RGB_off(RGB, length):
    for i in range(length):
        RGB[i] = (0, 0, 0)
        RGB.write()
        
def convert(value):
    volts = value * (3.3 / 65535)
    return volts

oil = 1
hydro = 2
wind = 3

solar = 1
coal = 2
nuclear = 3


while True:
    """
    val1 =  random.randint(1,255)
    val2 =  random.randint(1,255)
    val3 =  random.randint(1,255)
    """
    
    bad = recieve.value()
    #bad = 0
    energy = 0
    
    data1 = math.floor(convert(ADC(27).read_u16()))
    data2 = math.floor(convert(ADC(26).read_u16()))
    
    print(data1)
    print(data2)
    
    #check sources  
    if data1 == oil:
        energy += 3
        bad = 1
    elif data1 == hydro or data1 == wind:
        energy += 1
        
    if data2 == coal:
        energy += 3
        bad = 1
    elif data2 == nuclear:
        energy += 5
    elif data2 == solar:
        energy += 1
    
    turn_RGB_off(data_lvl, 10)
    for i in range(min(energy, 10)):
        data_lvl[i] = (255, 255, 255)
    data_lvl.write()
    
    #displaying dc lights
    if energy > 10:
        for i in range(19):
            da[i] = (255, 0, 0)
        da.write()
        sleep(.5)
        for i in range(19):
            da[i] = (255, 255, 255)
        da.write()
        sleep(.5)
    elif energy == 0:
        turn_RGB_off(da, 19)
    elif energy == 10:
        change_white(da, 19)
    elif 0 < energy < 10:
        brightness = int((255 * (energy/10)))
        turn_RGB_off(da, 19)
        
        for i in range(19):
            if i % (10 - energy) == 0:
                da[i] = (brightness, brightness, brightness)
        da.write()
    
    else:
        turn_RGB_off(da, 11)
    
    # enviroment
    #print(bad)
    if bad:
        change_red(en1, 29)
        change_red(en2, 29)
    else:
        """
        for i in range(29):
            en1[i] = (val1, val2, val3)
            en2[i] = (val1, val2, val3)
        en2.write()
        en1.write()
        """
        change_green(en1, 29)
        change_green(en2, 29)
        
    sleep(.1)