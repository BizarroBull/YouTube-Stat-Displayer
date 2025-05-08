# Bull's YouTube Statistics Displayer

:cow: :movie_camera: :100: :1234:

A device to display statistics for your YouTube channel.

<img title="Bull's YouTube Statistics Displayer" src="bysd.jpg">

The device will connect to the internet via a WiFi connection.
Every 60 seconds the device will request your YouTube statistics.
The result is displayed.<br>
Press the A button for light mode.<br>
Press the B button for dark mode.<br>


## What You Need

- Raspberry Pi Pico WH https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html
- Pimoroni Pico Display Pack 2.8" https://shop.pimoroni.com/products/pico-display-pack-2-8
- YouTube Channel ID
- Google API key
- WiFi credentials


## Get your channel ID

1. Sign in to YouTube. https://www.youtube.com/
2. In the top right, select your profile picture and then Settings.
3. From the left menu, select Advanced settings.
4. You’ll see your channel’s user and channel IDs.

Note: You must be signed in as the channel's primary owner to see this info.


## Get your API key

1. Go to the API Console. https://console.developers.google.com/
2. From the projects list, select a project or create a new one.
3. If the APIs & services page isn't already open, open the left side menu and select APIs & services.
4. On the left, choose Credentials.
5. Click Create credentials and then select API key.


## Enable YouTube v3 api

1. Go to the API Console. https://console.developers.google.com/
2. From the projects list, select your project that you created the API key for.
3. If the APIs & services page isn't already open, open the left side menu and select APIs & services.
4. On the left, choose Enabled APIs & services.
5. Click Enable APIs and services.
6. Click YouTube Data API v3
7. Click Enable.


## Testing your channel ID and API key

You can confirm your channel ID and API key are correct by using them in place of "channel_id" and "api_key" in the following link:

https://www.googleapis.com/youtube/v3/channels?part=statistics&id=channel_id&key=api_key


## Installing Software

The software is written in MicroPython. To install, you will need to install the Pirmoroni custom build of MicroPython as well as Thonny.
Detailed instructions can be found at https://learn.pimoroni.com/article/getting-started-with-pico

The latest version of the custom MicroPython is currently v1.24.0 beta 2.

Edit the config.py file and enter your WiFi credentials, channel name, channel ID, and API key.

Upload main.py, config.py, hourglass.png, ytlight.png and ytdark.png to the pico using Thonny.

Power cycle the pico and your YouTube statistics should be displayed.


## References

- [get YouTube channel ID](https://support.google.com/youtube/answer/3250431?hl=en)
- [create API key](https://support.google.com/googleapi/answer/6158862?hl=en)
- [YouTube logo](https://www.youtube.com/howyoutubeworks/resources/brand-resources/#logos-icons-and-colors)
- [Raspberry Pi Pico W: Getting Started with HTTP GET Requests (MicroPython)](https://randomnerdtutorials.com/raspberry-pi-pico-w-http-requests-micropython/)
- [hourglass icon](https://www.freepik.com/icon/hourglass_5582221)
