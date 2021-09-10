import math
import random
import time
from rpi_ws281x import *
import argparse

x = 12  # Number of LEDs in a unit distance
a = list(range(5 * x))
b_0 = list(range(a[-1] + 1, a[-1] + 1 + 4 * x))
b_1 = list(range(b_0[-1] + 1, b_0[-1] + 1 + 4 * x))
c_0 = list(range(b_1[-1] + 1, b_1[-1] + 1 + 3 * x))
c_1 = list(range(c_0[-1] + 1, c_0[-1] + 1 + 3 * x))
d_0 = list(range(c_1[-1] + 1, c_1[-1] + 1 + 2 * x))
d_1 = list(range(d_0[-1] + 1, d_0[-1] + 1 + 2 * x))
e_0 = list(range(d_1[-1] + 1, d_1[-1] + 1 + x))
e_1 = list(range(e_0[-1] + 1, e_0[-1] + 1 + x))

vertical_indices = a + b_1 + c_1 + d_1 + e_1
horizontal_indices = b_0 + c_0 + d_0 + e_0
all_indices = list(range(LED_COUNT))

all_segments = [a, b_0, b_1, c_0, c_1, d_0, d_1, e_0, e_1]

# LED strip configuration:
LED_COUNT      = 300     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 150      # Set to 0 for darkest and 255 for brightest
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

def colorWipe(strip, color=Color(255,0,0), wait_ms=10):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000)
        
def wheelPalette(state, palette):
    return Color(palette[state][0], palette[state][1], palette[state][2])
        
def colorEdge(strip, seq, color = Color(0, 255, 0)):
    for pos in seq:
        strip.setPixelColor(pos, color)
    
def cleanEdge(strip, seq):
    for pos in seq:
        strip.setPixelColor(pos, 0)
       
def soiree(strip, palette = neonPalette, numSeq = 3, freq = 2, tmax=100):
    segs = all_segments
    wait_s=1/freq
    N = [random.randint(0, len(segs)-1) for i in range(numSeq)]
    t=0
    while t<tmax:
        states = [random.randint(0, len(palette)-1) for i in range(numSeq)]
        
        for i in range(len(N)):
            colorEdge(strip, seq = segs[N[i]], color = wheelPalette(states[i], palette))
        strip.show()
        time.sleep(wait_s)
        for i in range(len(N)):
            cleanEdge(strip, seq = segs[N[i]])
        strip.show()
        
        N2 = [random.randint(0, len(segs)-1) for i in range(numSeq)]
        for i in range(len(N2)):
            A = N2[:i] + N2[i+1:]
            while (N2[i] in N) or (N2[i] in A):
                N2[i] = random.randint(0, len(segs)-1)
        t+=1
        N = N2


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            print('La Petite Coloc est dans la boucle')
            print("neon")
            soiree(strip, palette = neonPalette, freq = 7, tmax=30)
            print("mirror Edge")
            soiree(strip, palette = mirrorEdgePalette, freq = 7, tmax=30)
            print("africa")
            soiree(strip, palette = africaPalette, freq = 7, tmax=30)
            print("red to purple")
            soiree(strip, palette = redtopurplePalette, freq = 7, tmax=30)


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
