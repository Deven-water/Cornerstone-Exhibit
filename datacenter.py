from machine import Pin, PWM
from utime import sleep
import machine, neopixel
from machine import ADC
import math
import random
# test

da = neopixel.NeoPixel(machine.Pin(13), 19)
en1 = neopixel.NeoPixel(machine.Pin(0), 29)
en2 = neopixel.NeoPixel(machine.Pin(1), 29)

recieve = Pin(15, Pin.IN)
recieve2 = Pin(12, Pin.IN)
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

while True:
    bad = recieve.value()
    vill_win = recieve2.value()
    #bad = 0
    energy = 0
    
    data1 = round(convert(ADC(27).read_u16()), 2)
    data2 = round(convert(ADC(26).read_u16()), 2)
    
    #print(data1)
    #print(data2)
    
    #data1 
    if 1.6 < data1 < 1.7: # wind = 1.6/1.7
        energy += 2
    elif data1 > 3.2: #coal = 3.3
        energy += 3
        bad = 1
    elif 2.35 < data1 < 2.5: #Hydro = 2.4
       energy += 2
    elif 1.75 < data1 < 1.85:
        energy += 5 #hydro + wind = 1.8
        
    #data2   
    if 2.3 < data2 < 2.5: #solar = 2.4
        energy += 1
    elif data2 > 3.2: #nuclear = 3.3
        energy += 5
    elif 1.5 < data2 < 1.8: #oil = 1.6/1.7
        energy += 3
        bad = 1
    elif 2.15 < data2 < 2.3:
        energy += 8 # oil + nuclear = 2.7/2.8
        bad = 1
    elif 3.0 < data2 < 3.1: # solar + nuclear = 3
        energy += 6
        
    for i in range(10):
        data_lvl[i] = (0, 0, 0)
    for i in range(min(energy, 10)):
        data_lvl[i] = (125,125, 125)
    data_lvl.write()
    
    print(energy)
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
        change_green(en1, 29)
        change_green(en2, 29)
    
    if energy == 10 and not bad and vill_win:
        val1 =  random.randint(1,255)
        val2 =  random.randint(1,255)
        val3 =  random.randint(1,255)
        
        for i in range(29):
            en1[i] = (val1, val2, val3)
            en2[i] = (val1, val2, val3)
        en2.write()
        en1.write()
        
        sleep(.1)
        
    sleep(.1)