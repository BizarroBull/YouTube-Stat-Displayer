# Bull's YouTube Stat Displayer

title1 = "Bull's YouTube"
title2 = "Stat Displayer"
version = "v1.1.0"

# import machine
import time
from machine import Pin
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332
import pngdec
from pimoroni import RGBLED
import network
import requests

from config import WIFI_SSID, WIFI_PASSWORD, YT_CHANNEL, YT_CHANNEL_ID, YT_API_KEY


COLUMN_0 = 15
LINE_0 = 80
LINE_1 = 110
LINE_2 = 140
LINE_3 = 170

subscriberCount = '0'
viewCount = '0'

button_a = Pin(12, Pin.IN, Pin.PULL_UP)
button_b = Pin(13, Pin.IN, Pin.PULL_UP)
button_x = Pin(14, Pin.IN, Pin.PULL_UP)
button_y = Pin(15, Pin.IN, Pin.PULL_UP)

led = RGBLED(26, 27, 28)

# ------------------------------------------------------------------------------

def connect():
    global display
    global png
    global WHITE
    global BLACK
    rotation = 0
    waittime = 0

    try:
        # Open our PNG File from flash.
        png.open_file("hourglass.png")

        # Handle the error if the image doesn't exist on the flash.
    except OSError:
        print("Error: PNG File missing. Copy the PNG file to your Pico.")

    display.update()
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect( WIFI_SSID, WIFI_PASSWORD )
    while wlan.isconnected() == False:
        display.text( "Connecting to Wifi", COLUMN_0, LINE_1 )
        display.update()

        # Decode our PNG file and set the X and Y
        display.set_pen(BG)
        display.rectangle(260, 115, 16, 16)
        png.decode(260, 115, scale=1, rotate=rotation)
        rotation += 90
        if( rotation == 360 ):
            rotation = 0

        display.update()
        # print('Waiting for connection...')
        time.sleep(1)
        waittime = waittime + 1
        if( waittime == 10 ):
            machine.reset()

    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    display.set_pen(BLACK)
    display.text( f'Connected on', COLUMN_0, LINE_2 )
    display.text( f'{ip}', COLUMN_0, LINE_3 )
    display.update()
    time.sleep(1)

# ------------------------------------------------------------------------------

def get_yt_data():
    global subscriberCount
    global viewCount

    url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={YT_CHANNEL_ID}&key={YT_API_KEY}'
    # Make GET request
    response = requests.get(url)
    # Get response code
    # response_code = response.status_code
    # Get response content
    ytstats = response.json()
    # Close the request
    response.close()
    # Get channel specific data
    subscriberCount = ytstats['items'][0]['statistics']['subscriberCount']
    viewCount = ytstats['items'][0]['statistics']['viewCount']

# ------------------------------------------------------------------------------

def init_display():
    global display
    global WHITE
    global BLACK

    # Clear the screen

    display.set_pen(WHITE)
    display.clear()

    display.set_pen(BLACK)
    display.set_font("bitmap14_outline")
    display.text( f"{title1}", 5, 5 )
    display.text( f"{title2}", 5, 35 )
    display.text( f"{version}", 5, 65 )
    display.update()

# ------------------------------------------------------------------------------

def load_logo():
    global logo
    try:
        # Open our PNG File from flash.

        png.open_file( f"{logo}" )

        # Decode our PNG file and set the X and Y
        png.decode(10, 10, scale=1)

    # Handle the error if the image doesn't exist on the flash.
    except OSError:
        print("Error: PNG File missing. Copy the PNG file to your Pico.")

# ------------------------------------------------------------------------------

def update_display():
    global display
    global BG
    global TEXT
    global png

    # Clear the screen

    display.set_pen(BG)
    display.clear()

    display.set_pen(TEXT)
    display.set_font("bitmap14_outline")
    display.text( f'@{YT_CHANNEL}', COLUMN_0, LINE_0 )
    display.text( f'Subscribers: {subscriberCount}', COLUMN_0, LINE_1 )
    display.text( f'Total Views: {viewCount}', COLUMN_0, LINE_2 )

    # Decode our PNG file and set the X and Y

    png.decode(10, 10, scale=1)

    display.update()

# ------------------------------------------------------------------------------

# Create a PicoGraphics instance

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332)

# Create an instance of the PNG Decoder

png = pngdec.PNG(display)

# Set the backlight so we can see it.

display.set_backlight(1.0)

# Create some pens.

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

# Turn off the RGB LED

led.set_rgb(0, 0, 0)

BG = WHITE
TEXT = BLACK
countdowntimer = 0
init_display()
connect()
logo = "ytlight.png"
load_logo()

while True:

    if countdowntimer == 0:
        # One minute has passed.

        countdowntimer = 600;

        # Get updated YouTube data and update the display.

        get_yt_data()
        update_display();

    elif button_a.value() == 0:
        # Button A was pressed.
        # White background, black text.

        BG = WHITE
        TEXT = BLACK
        logo = "ytlight.png"
        load_logo()
        update_display();

    elif button_b.value() == 0:
        # Button B was pressed.
        # Black background, white text.

        BG = BLACK
        TEXT = WHITE
        logo = "ytdark.png"
        load_logo()
        update_display();


    # Sleep for 100ms then check buttons again.
    time.sleep(0.1)

    # Decrement our countdown timer.

    countdowntimer = countdowntimer - 1
