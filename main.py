#TODO ricordati di cancellare microdot dalla root
from libs.microdot.microdot import Microdot
import libs.effects as effects
import micropython
import network
import machine
import neopixel
import time

# import os
# print(os.uname())
micropython.mem_info()

# CONST
# NETWORK
NETWORK_SSID = 'i_have_a_link'
NETWORK_PASS = 'G8U9URxf6trUPe4'
# LED
n_leds_total = 32
PIN = 5  # d1
LED_COLOR_DEFAULT = (0, 200, 0)  # green
LED_COLOR_NETWORK_NOT_CONNECTED = (2, 2, 0)  # yellow
# config
NUM_LED = 40
# set np
np = neopixel.NeoPixel(machine.Pin(PIN), NUM_LED)
thread_run:bool=False
thread_wait:bool=False


# setup network
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        effects.set_led_color_fade(np,LED_COLOR_NETWORK_NOT_CONNECTED)
        sta_if.active(True)
        sta_if.connect(NETWORK_SSID, NETWORK_PASS)
        while not sta_if.isconnected():
            pass
        # network is connected
        effects.set_led_color_fade(np,LED_COLOR_DEFAULT)
    print('network config:', sta_if.ifconfig())


# setup webserver
app = Microdot()


def start_server():
    print('Starting microdot app')
    try:
        app.run(port=80)
    except:
        app.shutdown()

# api methods 
@app.get('/meminfo')
async def hello1(request):
    print(micropython.mem_info())


@app.get('/leds/setred')
async def hello2(request):
    effects.set_led_color_red(np)


@app.get('/leds/setgreen')
async def hello3(request):
    effects.set_led_color_green(np)

@app.get('/leds/setcolor/r/<int:red>/g/<int:green>/b/<int:blue>')
async def hello4(request,red,green,blue):
    effects.set_led_color_fade(np,(red, green, blue))

# @app.get('/leds/switchoff')
# async def hello5(request):
#     effects.set_led_color_fade(np,(0, 0, 0))

# @app.get('/leds/circle')
# async def hello6(request):
#     current_color=np[0]
#     effects.cycle(np,np[0][0],np[0][1],np[0][2],4)
#     effects.set_led_color(np,current_color)

# @app.get('/leds/bounce')
# async def hello7(request):
#     current_color=np[0]
#     effects.bounce(np,np[0][0],np[0][1],np[0][2],4)
#     effects.set_led_color(np,current_color)

@app.get('/leds/rmbwcircle')
async def hello8(request):
    print("hello8")
    global thread_run, thread_wait
    thread_run = False
    while thread_wait:
        print("hello8_wait")
        pass
    thread_run = True
    while thread_run:
        print("hello8_thread_run")
        thread_wait=True
        effects.rainbow_cycle(np,5)
        thread_wait=False

@app.get('/leds/setcolor/o/r1/<int:red1>/g1/<int:green1>/b1/<int:blue1>/r2/<int:red2>/g2/<int:green2>/b2/<int:blue2>')
async def hello9(request,red1,green1,blue1,red2,green2,blue2):
    effects.set_led_color_half_o(np,NUM_LED,(red1, green1, blue1),(red2, green2, blue2))

@app.get('/leds/setcolor/two/r1/<int:red1>/g1/<int:green1>/b1/<int:blue1>/r2/<int:red2>/g2/<int:green2>/b2/<int:blue2>')
async def hello10(request,red1,green1,blue1,red2,green2,blue2):
    effects.set_led_color_two(np,NUM_LED,(red1, green1, blue1),(red2, green2, blue2))

@app.get('/leds/twinkle/r/<int:red>/g/<int:green>/b/<int:blue>/w/<int:wait>')
async def hello12(request,red,green,blue,wait):
    print("hello12")
    global thread_run, thread_wait
    thread_run = False
    while thread_wait:
        print("hello12_wait")
        pass
    thread_run = True
    while thread_run:
        print("hello12_thread_run")
        thread_wait=True
        effects.twinkle(np,NUM_LED,(red, green, blue),wait)
        thread_wait=False

# main
do_connect()
start_server()
