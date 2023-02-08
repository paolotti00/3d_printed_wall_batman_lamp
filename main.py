from libs.microdot.microdot import Microdot
from libs.effects import write_fade_in
from libs.effects import cycle
from libs.effects import bounce
from libs.effects import rainbow_cycle
import micropython
import network
import machine
import neopixel

# import os
# print(os.uname())
micropython.mem_info()

# CONST
# NETWORK
NETWORK_SSID = 'i_have_a_link'
NETWORK_PASS = 'G8U9URxf6trUPe4'
# LED
n_leds_total = 32
N_LEDS_HEAD_POSITION = 31
N_LEDS_WING_SX_START = 0
N_LEDS_WING_SX_END = 15
N_LEDS_WING_DX_START = 16
N_LEDS_WING_DX_END = 30
PIN = 5  # d1
LED_COLOR_DEFAULT = (0, 2, 0)  # green
LED_COLOR_NETWORK_NOT_CONNECTED = (2, 2, 0)  # yellow
# config
N = 40
# set np
np = neopixel.NeoPixel(machine.Pin(PIN), N)


# setup network
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        set_led_color_fade(LED_COLOR_NETWORK_NOT_CONNECTED)
        sta_if.active(True)
        sta_if.connect(NETWORK_SSID, NETWORK_PASS)
        while not sta_if.isconnected():
            pass
        # network is connected
        set_led_color_fade(LED_COLOR_DEFAULT)
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
async def hello(request):
    return micropython.mem_info()


@app.get('/leds/setred')
async def hello(request):
    set_led_color_red()


@app.get('/leds/setgreen')
async def hello(request):
    set_led_color_green()

@app.get('/leds/setcolor/r/<int:red>/g/<int:green>/b/<int:blue>')
async def hello(request,red,green,blue):
    set_led_color_fade((red, green, blue))

@app.get('/leds/switchoff')
async def hello(request):
    set_led_color_fade((0, 0, 0))

@app.get('/leds/circle')
async def hello(request):
    current_color=np[0]
    cycle(np,np[0][0],np[0][1],np[0][2],4)
    set_led_color(current_color)

@app.get('/leds/bounce')
async def hello(request):
    current_color=np[0]
    bounce(np,np[0][0],np[0][1],np[0][2],4)
    set_led_color(current_color)

@app.get('/leds/rmbwcircle')
async def hello(request):
    rainbow_cycle(np,5)

# methods
def set_led_color_red():
    set_led_color_fade((128, 0, 0))

def set_led_color_green():
    set_led_color_fade((0, 255, 0))

def set_led_color_fade(rgb_color): # it accepted rgb_color like (0,255,0)
    np.fill(rgb_color)
    write_fade_in(np)

def set_led_color(rgb_color): # it accepted rgb_color like (0,255,0)
    np.fill(rgb_color)
    np.write()

# main
do_connect()
start_server()
