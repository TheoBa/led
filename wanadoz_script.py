from wanadoz_library import *


def main():
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
            colorWipe(strip, color=Color(255, 0, 255), wait_ms=1)
            colorWipe(strip, color=Color(0, 255, 0), wait_ms=1)
            

    except KeyboardInterrupt:
        if args.clear:
            kill(strip, color=Color(0,0,0))



# Main program logic follows:
if __name__ == '__main__':
    main()