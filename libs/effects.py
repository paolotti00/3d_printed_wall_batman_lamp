import math
import neopixel
import time
import math
from libs.bpm_reader import BMPReader
import uasyncio as asyncio
import random
import os

# close all np


def clear(np):
    n = np.n
    for i in range(n):
        np[i] = (0, 0, 0)
        np.write()


def cycle(np, r, g, b, wait):
    n = np.n
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (r, g, b)
        np.write()
        time.sleep_ms(wait)

# rainbow effect


def wheel(pos):
    #  Input a value 0 to 255 to get a color value.
    #  The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


async def rainbow_cycle(np, wait):
    n = np.n
    for j in range(255):
        for i in range(n):
            rc_index = (i * 256 // n) + j
            np[i] = wheel(rc_index & 255)
        np.write()
        await asyncio.sleep(wait)


def write_fade_in(np):
    brightness_step_division = [24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 1]
    # iterate step division
    for i, step_division in enumerate(brightness_step_division):
        new_np = neopixel.NeoPixel(np.pin, np.n)
        # print('--------')
        # print("step division = " + str(step_division))
        # iterate original np tuple
        for j, tuple in enumerate(np):
            # print('--------')
            # print("tuple j = "+str(j) + " tuple = " + str(tuple))
            tuple_item_list = []
            # interate single np tuple element
            for z, tuple_item in enumerate(tuple):
                # print ("tuple_item z = "+str(z) + " item = " + str(tuple_item))
                if(tuple_item != 0):
                    tuple_item_list.append(math.ceil(tuple_item/step_division))
                else:
                    tuple_item_list.append(0)
                # print ("tuple_item_list z = "+str(z) + " item = " + str(tuple_item_list[z]))
            new_np[j] = tuple_item_list
            # for x,new_tuple in enumerate(new_np):
            # print("new tuple " + str(new_tuple))
        # print("---------write--------")
        time.sleep_ms(1)
        new_np.write()


async def police(np, num_led):
    WAIT_TIME = 0.2  # Tempo di attesa tra un'iterazione e l'altra
    COLOR_1 = (255, 0, 0)  # Primo colore (rosso)
    COLOR_2 = (0, 0, 255)  # Secondo colore (blu)
    # Gradiente rosso-blu
    for i in range(num_led):
        r = int((num_led - i) * COLOR_1[0] /
                num_led + i * COLOR_2[0] / num_led)
        g = int((num_led - i) * COLOR_1[1] /
                num_led + i * COLOR_2[1] / num_led)
        b = int((num_led - i) * COLOR_1[2] /
                num_led + i * COLOR_2[2] / num_led)
        np[i] = (r, g, b)
    np.write()
    await asyncio.sleep(WAIT_TIME)

    # Gradiente blu-rosso
    for i in range(num_led):
        r = int((num_led - i) * COLOR_2[0] /
                num_led + i * COLOR_1[0] / num_led)
        g = int((num_led - i) * COLOR_2[1] /
                num_led + i * COLOR_1[1] / num_led)
        b = int((num_led - i) * COLOR_2[2] /
                num_led + i * COLOR_1[2] / num_led)
        np[i] = (r, g, b)
    np.write()
    await asyncio.sleep(WAIT_TIME)


async def tow_color_fade(np, num_led):
    WAIT_TIME = 0.09  # wating time between one excution and the next
    COLOR_1 = (255, 0, 0)  # first color (red)
    COLOR_2 = (0, 0, 255)  # second color (blue)
    # fading red-blue
    for i in range(num_led):
        r = int((num_led - i) * COLOR_1[0] /
                num_led + i * COLOR_2[0] / num_led)
        g = int((num_led - i) * COLOR_1[1] /
                num_led + i * COLOR_2[1] / num_led)
        b = int((num_led - i) * COLOR_1[2] /
                num_led + i * COLOR_2[2] / num_led)
        np[i] = (r, g, b)
        np.write()
        await asyncio.sleep(WAIT_TIME)

    # fading blue-red
    for i in range(num_led):
        r = int((num_led - i) * COLOR_2[0] /
                num_led + i * COLOR_1[0] / num_led)
        g = int((num_led - i) * COLOR_2[1] /
                num_led + i * COLOR_1[1] / num_led)
        b = int((num_led - i) * COLOR_2[2] /
                num_led + i * COLOR_1[2] / num_led)
        np[i] = (r, g, b)
        np.write()
        await asyncio.sleep(WAIT_TIME)


async def twinkle(np, num_led, rgb_color, wait):
    for i in range(num_led):
        np[i] = (rgb_color)
        np.write()
        await asyncio.sleep(wait)
        np[i] = (0, 0, 0)
        np.write()
        (wait)


async def candle(np, num_led):
    # Configurazione effetto candele
    MIN_BRIGHTNESS = 1
    MAX_BRIGHTNESS = 50
    FREQUENCY = 0.05
    for i in range(num_led):
            # Calcola la luminosità di base
            base_brightness = random.getrandbits(8)

            # Calcola una fluttuazione aggiuntiva della luminosità
            flicker = int((int.from_bytes(os.urandom(1), 'big') % 10 * 2 - 1) *
                          (MAX_BRIGHTNESS - MIN_BRIGHTNESS) / 2)
            brightness = max(MIN_BRIGHTNESS, min(
                base_brightness + flicker, MAX_BRIGHTNESS))

            # Imposta il colore dei LED sulla base della luminosità
            color = (brightness, int(brightness / 3), 0)
            np[i] = color

            # Aggiorna i LED Strip
            np.write()
    # Attendere prima di generare un nuovo frame
    await asyncio.sleep(FREQUENCY)
# methods


def set_led_color_red(np):
    set_led_color_fade(np, (128, 0, 0))


def set_led_color_green(np):
    set_led_color_fade(np, (0, 255, 0))


def set_led_color_fade(np, rgb_color):  # it accepted rgb_color like (0,255,0)
    np.fill(rgb_color)
    write_fade_in(np)


def set_led_color(np, rgb_color):  # it accepted rgb_color like (0,255,0)
    np.fill(rgb_color)
    np.write()


def set_led_color_half_o(np, num_led, rgb_color_a, rgb_color_b):
    for pixel_id in range(0, num_led/2):
        np[pixel_id] = rgb_color_a
        time.sleep_ms(2)
        np.write()
    for pixel_id in range(num_led/2, num_led):
        np[pixel_id] = rgb_color_b
        time.sleep_ms(2)
        np.write()


def set_led_color_two(np, num_led, rgb_color_a, rgb_color_b):
    clear(np)
    current_color = rgb_color_b
    for i in range(0, num_led, 5):
        current_color = rgb_color_a if current_color == rgb_color_b else rgb_color_b
        for y in range(i-5, i):
            np[y] = current_color
            time.sleep_ms(2)
            np.write()
