# TODO ricordati di cancellare microdot dalla root
import uasyncio as asyncio
import libs.tinyweb as tinyweb
import libs.effects as effects
import micropython
import network
import machine
import neopixel
import time
import gc
import ujson
from umqtt.simple import MQTTClient

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
current_effect_task: any = None


# setup network
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        effects.set_led_color_fade(np, LED_COLOR_NETWORK_NOT_CONNECTED)
        sta_if.active(True)
        sta_if.connect(NETWORK_SSID, NETWORK_PASS)
        while not sta_if.isconnected():
            pass
        # network is connected
        effects.set_led_color_fade(np, LED_COLOR_DEFAULT)
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


@app.route('/')
async def mem_info(request, response: tinyweb.response):
    await response.send_file("static/index.html")



@app.resource('/effect', method='POST')
async def effect(request):
    print(request)
    asyncio.get_event_loop().create_task(effect_handler(request))
    print('dopo asyncio.run(effect_handler(request))')
    return {'ok': 'ok'}, 200


async def effect_handler(request):
    global current_effect_task
    print("effect_handler received: "+str(request))
    new_effect_name = request['name']
    print(new_effect_name)
    # check if other effect task is running and stop it
    if (not current_effect_task == None) and not (current_effect_task.done()):
        # is running we have to stop it
        # print(current_effect_task.get_name() + " is running we will cancel it") #todo
        print("the task is running")
        if current_effect_task.cancel():
            # print(current_effect_task.get_name() + " was cancelled") #todo
            print("the task was cancelled")
        else:
            # print(current_effect_task.get_name() + " was not cancelled") #todo
            print("the task was cancelled")
    if new_effect_name == 'rainbow_cycle':
        wait = get_wait_from_request(request, False)
        current_effect_task = asyncio.get_event_loop().create_task(
            looppa(effects.rainbow_cycle, np, wait))
    if new_effect_name == 'twinkle':
        wait = get_wait_from_request(request, False)
        color = get_color_from_request(request, True)
        current_effect_task = asyncio.get_event_loop().create_task(
            looppa(effects.twinkle, np, NUM_LED, color, wait))
    if new_effect_name == 'police':
        wait = get_wait_from_request(request, False)
        current_effect_task = asyncio.get_event_loop().create_task(
            looppa(effects.police, np, NUM_LED))
    if new_effect_name == 'tow_color_fade':
        wait = get_wait_from_request(request, False)
        current_effect_task = asyncio.get_event_loop().create_task(
            looppa(effects.tow_color_fade, np, NUM_LED))
    if new_effect_name == 'candle':
        wait = get_wait_from_request(request, False)
        current_effect_task = asyncio.get_event_loop().create_task(
            looppa(effects.candle, np, NUM_LED))


async def looppa(l, *args):
    print(*args)
    while True:
        await l(*args)
        print('loop')
        # await asyncio.sleep(0.1)


def get_effect_data_from_request(request, mandatory):
    effect_data = None
    if 'effect_data' in request:
        effect_data = request['effect_data']
    elif mandatory:
        raise Exception("error no effect_data in request")
    # returning None
    print("effect_data returned " + str(effect_data))
    return effect_data


def get_color_from_request(request, mandatory):
    effect_data = get_effect_data_from_request(request, mandatory)
    if (not effect_data == None) and ('color' in effect_data):
        r = int(effect_data['color'].split(",")[0])
        g = int(effect_data['color'].split(",")[1])
        b = int(effect_data['color'].split(",")[2])
    elif mandatory:
        raise Exception("error no color in request")
    return (r, g, b)


def get_wait_from_request(request, mandatory):
    default_wait = 0.01
    effect_data = get_effect_data_from_request(request, mandatory)
    if (not effect_data == None) and ('wait' in effect_data):
        wait = float(effect_data['wait'])
    elif mandatory:
        raise Exception("error no wait in request")
    else:
        print("no wait in effect data, " + str(default_wait) +
              " as default will be returned")
        wait = default_wait
    return wait


# mqtt
MQTT_SERVER = "192.168.50.32"
MQTT_TOPIC = "light_effect"

client = MQTTClient("client_id", MQTT_SERVER)


def handle_mqtt_message(topic, message):
    try:
        print(message)
        # gestisce il messaggio MQTT per l'effetto di luce
        request_data = ujson.loads(message)
        print("request_data -->" + str(request_data))
        asyncio.get_event_loop().create_task(effect_handler(request_data))
    except Exception as e:
        print(e)
        pass
    print('mqtt end')


async def check_new_message(client):
    i = 0
    while True:
        i = i+1
        print("checking "+str(i))
        client.check_msg()
        await asyncio.sleep(0.5)

def mqtt_msg_received(topic, message):
    print ("mqtt_msg_received received "  + str(message))
# main
# wifi
do_connect()
#mqtt
client.connect()
client.set_callback(handle_mqtt_message)
client.subscribe(MQTT_TOPIC)
client.publish(MQTT_TOPIC, "acceso", retain=False, qos=0)
asyncio.get_event_loop().create_task(check_new_message(client))
# webserver
start_server()
