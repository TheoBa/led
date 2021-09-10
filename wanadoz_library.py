import time
import random as rd
from rpi_ws281x import *
import argparse
import random
import math


LED_COUNT      = 24*18     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    
rgbPalette = [(255,0,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (255,0,255)]
redtopurplePalette = [(255,0,0), (255,0,150), (80,150,255)]
vaporWavePalette = [(255,113,206), (1,205,254), (5,255,161), (185,103,255), (255,251,150)]
neonPalette = [(254,0,0), (253,254,2), (11,255,1), (1,30,254), (254,0,246)]
flamesPalette = [[0,255,0], [255,100,0], [255,0,0], [255,255,0]]
jamaRedPalette = [[255,0,0], [255,100,0], [255,0,0], [255,100,0]]
autumnPalette = [[244,134,0], [255,165,0], [255,153,102], [235,99,98], [238,59,57]]
africaPalette = [(20,253,83), (28,255,238), (253,26,243), (255,184,15), (253,8,8)]
seaPalette = [(70,130,255), (17,35,80), (34,70,150), (80,100,255), (30,40,80), (0, 0, 200)]
mirrorEdgePalette = [(253,17,17), (255,92,4), (251,232,22), (75,246,36), (13,52,193)]



def pos_to_px(pos):
    y = pos//24
    if y%2==0:
        x = pos%24
    else:
        x = 23 - pos%24
    return [x, y]

def px_to_pos(px):
    x = px[0]
    y = px[1]
    pos = y*24
    if y%2==0:
        pos += x
    else:
        pos += 23 - x
    return pos

def colorWipe(strip, color, wait_ms = 10):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000)

def rainbowWheel(pos):
    """pos in 0, 255"""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def circle_to_pos(n): # n is an int corresponding to the circle
    l_px = []
    if n>=0 and n<9:
        for i in range(n, 24-n):
            l_px.append([i, n])
        for j in range(n+1, 17-n):
            l_px.append([23-n, j])
        for i in range(n, 24-n):
            l_px.append([23-i, 17-n])
        for j in range(n+1, 17-n):
            l_px.append([n, 17-j])
        l_pos = [px_to_pos(px) for px in l_px]
        return l_pos
    else:
        return []

def circleWipe(strip, color, n_circle = 1, wait_ms = 10):
    l_pos = circle_to_pos(n_circle)
    for i in l_pos:
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000)

def circlesCenterToExterior(strip, wait_ms = 25, palette = mirrorEdgePalette):
    previous_pos = []
    for v in palette:
        color = Color(v[0], v[1], v[2])
        for n in range(9):
            for i in previous_pos:
                strip.setPixelColor(i, Color(0, 0, 0))
            l_pos = circle_to_pos(8-n)
            for i in l_pos:
                strip.setPixelColor(i, color)
            strip.show()
            previous_pos = l_pos
            
            time.sleep(wait_ms/1000)

def ambianceCenterToExterior(strip, wait_ms = 25, palette = mirrorEdgePalette):
    for v in palette:
        color = Color(v[0], v[1], v[2])
        for n in range(9):
            l_pos = circle_to_pos(8-n)
            for i in l_pos:
                strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms/1000)
        time.sleep(wait_ms/500)




def wheelPalette(state, palette):
    return Color(palette[state][0], palette[state][1], palette[state][2])

def kill(strip, color=Color(0,0,0)):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def colorRoudning(value):
    if value < 0:
        return 0
    elif value > 255:
        return 255
    else:
        return int(value)

def colorWheel(pos, palette):
    for i in range(2):
        palette = palette + palette
    n = len(palette) #nb of transitions
    if n == 0: #When palette is 1 color long
        return Color(palette[0][0], palette[0][1], palette[0][2])
    p = 256/n
    #general case one way
    for i in range(n-1):
        if i*p-1 <= pos and pos < (i+1)*p -1:
            pos -= i*p-1
            transitionR = colorRoudning(int(palette[i][0] + pos * (palette[i+1][0] - palette[i][0])/(p-1)))
            transitionG = colorRoudning(int(palette[i][1] + pos * (palette[i+1][1] - palette[i][1])/(p-1)))
            transitionB = colorRoudning(int(palette[i][2] + pos * (palette[i+1][2] - palette[i][2])/(p-1)))
            #print("aller", transitionR , transitionG, transitionB)
            return Color(transitionR , transitionG, transitionB)
    #final cycle
    #else:
    pos -= (n-1)*p-1
    transitionR = colorRoudning(int(palette[n-1][0] + pos * (palette[0][0] - palette[n-1][0])/(p-1)))
    transitionG = colorRoudning(int(palette[n-1][1] + pos * (palette[0][1] - palette[n-1][1])/(p-1)))
    transitionB = colorRoudning(int(palette[n-1][2] + pos * (palette[0][2] - palette[n-1][2])/(p-1)))
    #print("fin", transitionR , transitionG, transitionB)
    return Color(transitionR , transitionG, transitionB)

def colorCycle(strip, palette, timeStep):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, colorWheel((int(i * 256 / strip.numPixels() + timeStep)) & 255, palette))
