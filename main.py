#TODO ricordati di cancellare microdot dalla root
import uasyncio as asyncio
import libs.tinyweb as tinyweb
import libs.effects as effects
import micropython
import network
import machine
import neopixel
import time
import gc

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
current_effect_task:any


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
app = tinyweb.webserver()


def start_server():
    print('Starting microdot app')
    try:
         app.run(host='0.0.0.0', port=80)
    except:
        app.shutdown()

# api methods 
@app.route('/meminfo')
async def mem_info(request,response:tinyweb.response):
    print(micropython.mem_info())
    await response.start_html()
    # Send actual HTML page
    await response.send('<html><body><h1>Hello, world! free: {} allocated: {} </h1></html>\n'.format(gc.mem_free(), gc.mem_alloc()))
@app.resource('/effect',method='POST')
async def effect(request):
    print(request['data']) 
    print(request['data']['data1']) 
    
async def test(name):
    print(name)
    while True:
        print('true'+name)
        await asyncio.sleep(0.1)

# main
do_connect()
start_server()


