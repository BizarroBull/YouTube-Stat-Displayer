# Bull's YouTube Stat Displayer

title1 = "Bull's YouTube"
title2 = "Stat Displayer"
version = "v0.1.0"

# import machine
import time
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332
import pngdec

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

# ------------------------------------------------------------------------------

def connect():
    global display
    global png
    global BG
    global TEXT
    rotation = 0
    waittime = 0

    try:
        # Open our PNG File from flash. In this example we're using an image of a cartoon pencil.
        # You can use Thonny to transfer PNG Images to your Pico.
        png.open_file("hourglass.png")
        # png.open_file("yt_icon_rgb.png")

        # Decode our PNG file and set the X and Y
 #       png.decode(300, LINE_1, scale=1, rotate=90)

        # Handle the error if the image doesn't exist on the flash.
    except OSError:
        print("Error: PNG File missing. Copy the PNG file from the example folder to your Pico using Thonny and run the example again.")
    display.update()
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect( WIFI_SSID, WIFI_PASSWORD )
    while wlan.isconnected() == False:
        display.text( "Connecting to Wifi", COLUMN_0, LINE_1 )
        display.update()
        try:
            # Open our PNG File from flash. In this example we're using an image of a cartoon pencil.
            # You can use Thonny to transfer PNG Images to your Pico.
  #          png.open_file("hourglass.png")
            # png.open_file("yt_icon_rgb.png")

            # Decode our PNG file and set the X and Y
            display.set_pen(BG)
            display.rectangle(260, 115, 16, 16)
            png.decode(260, 115, scale=1, rotate=rotation)
            rotation += 90
            if( rotation == 360 ):
                rotation = 0

            # Handle the error if the image doesn't exist on the flash.
        except OSError:
            print("Error: PNG File missing. Copy the PNG file from the example folder to your Pico using Thonny and run the example again.")
        display.update()
        # print('Waiting for connection...')
        time.sleep(1)
        waittime = waittime + 1
        if( waittime == 10 ):
            machine.reset()

    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    display.set_pen(TEXT)
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
    # response_content = response.content
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
    global png
    global BG
    global TEXT
    global title

    # Create a PicoGraphics instance
    display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332)
    # Set the backlight so we can see it!
    display.set_backlight(1.0)

    # Create an instance of the PNG Decoder
    png = pngdec.PNG(display)

    # Create some pens for use later.
    BG = display.create_pen(255, 255, 255)
    TEXT = display.create_pen(0, 0, 0)

    # Clear the screen
    display.set_pen(BG)
    display.clear()

    display.set_pen(TEXT)
    display.set_font("bitmap14_outline")
    display.text( f"{title1}", 5, 5 )
    display.text( f"{title2}", 5, 35 )
    display.text( f"{version}", 5, 65 )
    display.update()

# ------------------------------------------------------------------------------

def update_display():
    global display
    global BG
    global TEXT

    # Set the backlight so we can see it!
    display.set_backlight(1.0)

    # Create an instance of the PNG Decoder
 #   png = pngdec.PNG(display)

    # Create some pens for use later.
    BG = display.create_pen(255, 255, 255)
    TEXT = display.create_pen(0, 0, 0)

    # Clear the screen
    display.set_pen(BG)
    display.clear()

    display.set_pen(TEXT)
    display.set_font("bitmap14_outline")
    #display.text( f'channel'"@antoniodio", 15, 80)
    display.text( f'@{YT_CHANNEL}', COLUMN_0, LINE_0 )
    display.text( f'Subscribers: {subscriberCount}', COLUMN_0, LINE_1 )
    display.text( f'Total Views: {viewCount}', COLUMN_0, LINE_2 )

    try:
        # Open our PNG File from flash. In this example we're using an image of a cartoon pencil.
        # You can use Thonny to transfer PNG Images to your Pico.
        png.open_file("ytlight.png")
        # png.open_file("yt_icon_rgb.png")

        # Decode our PNG file and set the X and Y
        png.decode(10, 10, scale=1)

    # Handle the error if the image doesn't exist on the flash.
    except OSError:
        print("Error: PNG File missing. Copy the PNG file from the example folder to your Pico using Thonny and run the example again.")

    display.update()

# ------------------------------------------------------------------------------

init_display()
connect()

while True:
    # Get updated YouTube data and update the display.

    get_yt_data()
    update_display();

    # Sleep for 60 seconds.

    time.sleep(60)
