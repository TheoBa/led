from tkinter import *
import time
import random as rd
# from rpi_ws281x import *
import argparse
import random
import math
from wanadoz_library import *

RADIUS_LED = 2
DIST_LED = 17
OFFSET_DRAWING_X = 50
OFFSET_DRAWING_Y = -75

seq = [i for i in range(24*18)]


positions = []
pixels = []

master = Tk()
canvas_width = 600
canvas_height = 400
master.title("LEDs WanaDoz")
# master.attributes("-fullscreen", True)
w = Canvas(master, width=canvas_width - 50, height=canvas_height - 50)


def paint(x, y, r, g, b):
    colorval = "#%02x%02x%02x" % (r, g, b)
    x1, y1 = (x - RADIUS_LED), (y - RADIUS_LED)
    x2, y2 = (x + RADIUS_LED), (y + RADIUS_LED)
    pixel = w.create_oval(x1, y1, x2, y2, fill=colorval, outline=colorval)
    pixels.append(pixel)


def repaint(i, r, g, b):
    colorval = "#%02x%02x%02x" % (r, g, b)
    pixel = pixels[i]
    w.itemconfig(pixel, fill=colorval, outline=colorval)
    x = positions[i][0]
    y = positions[i][1]
    if r == 0 and g == 0 and b == 0:
        x1, y1 = (x), (y)
        x2, y2 = (x), (y)
    else:
        x1, y1 = (x - RADIUS_LED), (y - RADIUS_LED)
        x2, y2 = (x + RADIUS_LED), (y + RADIUS_LED)
    w.coords(pixel, x1, y1, x2, y2)


class Strip:
    def __init__(self):
        return

    def begin(self):
        print("Lets start !")

    def numPixels(self):
        return LED_COUNT

    def setPixelColor(self, pixel, color):
        c = color
        if isinstance(color, int):
            c = [color, color, color]
        repaint(pixel, c[0], c[1], c[2])

    def show(self):
        w.update()

    def set_color_list(self, pixel_list, color):
        for pixel in pixel_list:
            self.setPixelColor(pixel, color)

def initialize():
    w.configure(background="black")
    for i in seq:
        
        y = i//24
        if y%2==0:
            x = i%24
        else:
            x = 23 - i%24 

        new_x = OFFSET_DRAWING_X + DIST_LED*x
        new_y = canvas_height + OFFSET_DRAWING_Y - DIST_LED*y
        paint(new_x, new_y, 255, 255, 255)
        positions.append([new_x, new_y])
        
            
###############
    
# I want to make circles that would 
class Circles():
    def __init__(self, strip) -> None:
        self.strip = strip



class Painting():
    hasEnded = False
    state = 0
    
    def __init__(self, strip, pos, radiusMax):
        self.strip = strip
        self.pos = pos
        self.radiusMax = radiusMax
        self.colorBase = 255*random.random()
                             
    def nextStep(self):
        self.strip.setPixelColor((self.pos + self.state)%self.strip.numPixels(), rainbowWheel(int(self.colorBase + 10*self.state)%255))
        self.strip.setPixelColor((self.pos - self.state)%self.strip.numPixels(), rainbowWheel(int(self.colorBase + 10*self.state)%255))
        self.state += 1

    def isFinished(self):
        if self.state == self.radiusMax:
            self.hasEnded = True
        return self.hasEnded

class Action():
    paintings = []
    paintings2 = [] #I am bad with memory issues lol
    def __init__(self, strip, frequency, radiusMax):
        self.strip = strip
        self.frequency = frequency
        self.radiusMax = radiusMax

    def makePainting(self):
        self.paintings.append(Painting(self.strip, int(self.strip.numPixels()*random.random()), self.radiusMax))

    def nextStep(self):
        if len(self.paintings) == 0:
            self.makePainting()
        else:
            A = random.random()
            if A / self.frequency < 0.1:
                self.makePainting()
        self.paintings2 = self.paintings
        for p in self.paintings:
            p.nextStep()
            if p.isFinished():
                self.paintings2.remove(p)
        self.paintings = self.paintings2

def Scenario(strip, bordel):
    bordel.nextStep()
    strip.show()
###

# Create NeoPixel object with appropriate configuration.
# strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip = Strip()

def run():
    print("Au niveau du nice..")
    while True:
        #### ENTRER LE NOM DE LA FONCTION CI-DESSOUS
        colorWipe(strip, color=Color(255, 0, 255), wait_ms=1)
        circlesCenterToExterior(strip, wait_ms = 50, palette = mirrorEdgePalette)
        ambianceCenterToExterior(strip, wait_ms = 25, palette = flamesPalette)

    print("Program ended")


w.pack(expand=YES, fill=BOTH)

b = Button(master, bg="white", fg="black", text="Run", command=run)
b.pack(expand=YES, fill=BOTH)

initialize()


mainloop()
