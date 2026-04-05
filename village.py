from machine import Pin, PWM
from utime import sleep
import machine, neopixel
from machine import ADC
import math

vill = neopixel.NeoPixel(machine.Pin(13), 29)
sender = Pin(15, Pin.OUT)
win = Pin(12, Pin.OUT)
# enviroment =  neopixel.NeoPixel(machine.Pin(0), 8)
# data center = neopixel.NeoPixel(machine.Pin(0), 8)
# village = neopixel.NeoPixel(machine.Pin(0), 8)

vill_lvl = neopixel.NeoPixel(machine.Pin(14), 5)

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
    sleep(.1)
        
def convert(value):
    volts = value * (3.3 / 65535)
    return volts

while True:
    sender.value(0)
    win.value(0)
    energy = 0
    
    village1 = round(convert(ADC(27).read_u16()), 2)
    village2 = round(convert(ADC(26).read_u16()), 2)
    
    print(village1)
    #print(village2)
    
    #village 1  
    if 1.5 < village1 < 1.65: #wind = 1.6/1.7
        energy += 2
    elif 1.9 < village1 < 2.1: # hydro = 2.0
        energy += 2
    elif village1 > 3.2: # oil = 3.3
        energy += 2
        sender.value(1)
    elif 1.7 < village1 < 1.8: # wind + hydro = 1.75
        energy += 5
        
    #village 2
    if 1.9 < village2 < 2.1: #solar = 2.0
        energy += 1
    elif 2.95 < village2 < 3.1: #nuclear = 3.3
        energy += 5
    elif 1.55 < village2 < 1.63: #oil = 1.6
        energy += 3
        sender.value(1)
    elif 1.7 < village2 < 1.8: # oil + solar = 1.8
        energy += 4
        sender.value(1)
    elif 2.1 < village2 < 2.2: # nuclear + oil = 2.1
        energy += 8
        sender.value(1)
    elif 2.8 < village2 < 2.9: # nuclear + solar = 2.8
        energy = 6
        
    for i in range(5):
        vill_lvl[i] = (0, 0, 0)
        
    for i in range(min(energy, 5)):
        vill_lvl[i] = (150, 0, 150)
    vill_lvl.write()
    
    if energy > 5:
        for i in range(29):
            vill[i] = (125, 0, 0)
        vill.write()
        sleep(.3)
        for i in range(29):
            vill[i] = (125, 125, 125)
        vill.write()
    elif energy == 0:
        turn_RGB_off(vill, 29)
    elif energy == 5:
        change_white(vill, 29)
        win.value(1)
    elif 0 < energy < 5:
        brightness = int((255 * (energy/10)))
        turn_RGB_off(vill, 29)
        
        for i in range(29):
            if i % (6 - energy) == 0:
                vill[i] = (brightness, brightness, brightness)
        vill.write()
    else:
        turn_RGB_off(vill, 29)
    
    
    sleep(.5)