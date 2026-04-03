from machine import Pin, PWM
from utime import sleep
import machine, neopixel
from machine import ADC
import math

vill = neopixel.NeoPixel(machine.Pin(13), 29)
sender = Pin(15, Pin.OUT)
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
        
def convert(value):
    volts = value * (3.3 / 65535)
    return volts

#vill1
coal = 2
hydro = 1
wind = 3

#vill2
solar = 2
oil = 1
nuclear = 3

while True:
    sender.value(0)
    energy = 0
    
    village1 = round(convert(ADC(27).read_u16()))
    village2 = round(convert(ADC(26).read_u16()))
    
    print(village1)
    print(village2)
    
    #village   
    if village1 == oil:
        energy += 3
        sender.value(1)
    elif village1 == hydro or village1 == wind:
        energy += 1

    if village2 == oil:
        energy += 3
        sender.value(1)
    elif village2 == nuclear:
        energy += 5
    elif village2 == solar:
        energy += 1
    
    print(energy)
    
    turn_RGB_off(vill_lvl, 5)
    for i in range(min(energy, 5)):
        vill_lvl[i] = (125, 125, 125)
    vill_lvl.write()
    
    if energy > 5:
        for i in range(29):
            vill[i] = (125, 0, 0)
        vill.write()
        sleep(.5)
        for i in range(29):
            vill[i] = (125, 125, 125)
        vill.write()
        sleep(.5)
    elif energy == 0:
        turn_RGB_off(vill, 29)
    elif energy == 5:
        change_white(vill, 29)
    elif 0 < energy < 5:
        brightness = int((255 * (energy/10)))
        turn_RGB_off(vill, 29)
        
        for i in range(29):
            if i % (5 - energy) == 0:
                vill[i] = (brightness, brightness, brightness)
        vill.write()
    else:
        turn_RGB_off(vill, 29)
    
    
    
    sleep(.5)